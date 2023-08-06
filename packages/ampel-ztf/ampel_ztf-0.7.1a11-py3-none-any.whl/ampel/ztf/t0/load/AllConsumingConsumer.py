#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/ztf/t0/alerts/AllConsumingConsumer.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : Unspecified
# Last Modified Date: 14.11.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import enum
import json
import sys
import time
import uuid
from typing import Optional

import confluent_kafka

from ampel.metrics.AmpelMetricsRegistry import AmpelMetricsRegistry


class KafkaMetrics:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._metrics = {
            # metrics relevant for read performance
            # see: https://github.com/edenhill/librdkafka/blob/master/STATISTICS.md
            # the most important of these is consumer_lag. to get an accurate count
            # from N balanced consumers running in separate processes, we have to:
            # - label by topic and partition (toppar)
            # - set gauge to -1 if this client is not assigned to the toppar
            # - create gauge in max mode (taking aggregated value for each toppar from the assigned process only)
            # - query sum(ampel_kafka_consumer_lag != -1) without (partition,topic)
            k: AmpelMetricsRegistry.gauge(
                k,
                "",
                subsystem="kafka",
                labelnames=("topic", "partition"),
                multiprocess_mode="max",
            )
            for k in (
                "fetchq_cnt",
                "fetchq_size",
                "consumer_lag",
                "rxmsgs",
                "rxbytes",
                "msgs_inflight",
            )
        }
        for action in "created", "consumed":
            self._metrics[f"last_message_{action}"] = AmpelMetricsRegistry.gauge(
                f"last_message_{action}",
                f"Timestamp when the most recent message was {action}",
                unit="timestamp",
                subsystem="kafka",
                multiprocess_mode="max",
            )

    def on_stats_callback(self, payload):
        for topic in json.loads(payload)["topics"].values():
            for partition in topic["partitions"].values():
                for k, v in partition.items():
                    if metric := self._metrics.get(k):
                        # only record value for assigned partitions (i.e. where desired is True)
                        metric.labels(topic["topic"], partition["partition"]).set(v if partition["desired"] else -1)

    def on_consume(self, message):
        kind, ts = message.timestamp()
        if kind == confluent_kafka.TIMESTAMP_CREATE_TIME:
            self._metrics["last_message_created"].set(ts / 1000)
        self._metrics["last_message_consumed"].set(time.time())


KafkaErrorCode = enum.IntEnum(  # type: ignore[misc]
    "KafkaErrorCode",
    {
        k: v
        for k, v in confluent_kafka.KafkaError.__dict__.items()
        if isinstance(v, int) and isinstance(k, str)
    },
)


class KafkaError(RuntimeError):
    """Picklable wrapper for cimpl.KafkaError"""

    def __init__(self, kafka_err):
        super().__init__(kafka_err.args[0])
        self.code = KafkaErrorCode(kafka_err.code())


class AllConsumingConsumer:
    """
    Consume messages on all topics beginning with 'ztf_'.
    """

    def __init__(self, broker, timeout=None, topics=["^ztf_.*"], **consumer_config):
        """ """

        self._metrics = KafkaMetrics.instance()
        config = {
            "bootstrap.servers": broker,
            "default.topic.config": {"auto.offset.reset": "smallest"},
            "enable.auto.commit": True,
            "receive.message.max.bytes": 2 ** 29,
            "auto.commit.interval.ms": 10000,
            "enable.auto.offset.store": False,
            "group.id": uuid.uuid1(),
            "enable.partition.eof": False,  # don't emit messages on EOF
            "topic.metadata.refresh.interval.ms": 1000,  # fetch new metadata every second to pick up topics quickly
            # "debug": "all",
            "stats_cb": self._metrics.on_stats_callback,
            "statistics.interval.ms": 10000,
        }
        config.update(**consumer_config)
        self._consumer = confluent_kafka.Consumer(**config)

        self._consumer.subscribe(topics)
        if timeout is None:
            self._poll_interval = 1
            self._poll_attempts = sys.maxsize
        else:
            self._poll_interval = max((1, min((30, timeout))))
            self._poll_attempts = max((1, int(timeout / self._poll_interval)))
        self._timeout = timeout

        self._last_message = None

    def __del__(self):
        # NB: have to explicitly call close() here to prevent
        # rd_kafka_consumer_close() from segfaulting. See:
        # https://github.com/confluentinc/confluent-kafka-python/issues/358
        self._consumer.close()

    def __next__(self):
        message = self.consume()
        if message is None:
            raise StopIteration
        else:
            return message

    def __iter__(self):
        return self

    def consume(self) -> Optional[confluent_kafka.Message]:
        """
        Block until one message has arrived, and return it.
        
        Messages returned to the caller marked for committal
        upon the _next_ call to consume().
        """
        # mark the last emitted message for committal
        if self._last_message is not None:
            self._consumer.store_offsets(self._last_message)
        self._last_message = None

        message = None
        for _ in range(self._poll_attempts):
            # wake up occasionally to catch SIGINT
            message = self._consumer.poll(self._poll_interval)
            if message is not None:
                if err := message.error():
                    if err.code() == confluent_kafka.KafkaError.UNKNOWN_TOPIC_OR_PART:
                        # ignore unknown topic messages
                        continue
                    elif err.code() in (
                        confluent_kafka.KafkaError._TIMED_OUT,
                        confluent_kafka.KafkaError._MAX_POLL_EXCEEDED,
                    ):
                        # bail on timeouts
                        return None
                break
        else:
            return message

        if message.error():
            raise KafkaError(message.error())
        else:
            self._last_message = message
            self._metrics.on_consume(message)
            return message
