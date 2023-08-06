#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/ztf/pipeline/t0/load/UWAlertLoader.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : Unspecified
# Last Modified Date: 25.03.2021
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

import io
import itertools
import logging
import time
import uuid
from collections import defaultdict
from typing import Any, DefaultDict, Dict, Iterator, List, Literal, Optional, TYPE_CHECKING

import fastavro
from pydantic import Field

from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.ztf.t0.load.AllConsumingConsumer import AllConsumingConsumer

log = logging.getLogger(__name__)


class UWAlertLoader(AmpelBaseModel):
    """
    Iterable class that loads avro alerts from the Kafka stream 
    provided by University of Washington (UW) 
    """
    #: Address of Kafka broker
    bootstrap: str = "partnership.alerts.ztf.uw.edu:9092"
    #: Alert steam to subscribe to
    stream: Literal["ztf_uw_private", "ztf_uw_public"] = "ztf_uw_public"
    #: Consumer group name
    group_name: str = str(uuid.uuid1())
    #: Alert archive client
    archive_updater: Any = None
    #: time to wait for messages before giving up, in seconds
    timeout: int = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        topics = ["^ztf_.*_programid1$"]

        if self.stream == "ztf_uw_private":
            topics.append("^ztf_.*_programid2$")
        config = {"group.id": f"{self.group_name}-{self.stream}"}

        self._consumer = AllConsumingConsumer(
            self.bootstrap, timeout=self.timeout, topics=topics, **config
        )

    def alerts(self, limit: Optional[int]=None) -> Iterator[io.BytesIO]:
        """
        Generate alerts until timeout is reached
        :returns: dict instance of the alert content
        :raises StopIteration: when next(fastavro.reader) has dried out
        """
        topic_stats: DefaultDict[str, List[float]] = defaultdict(lambda: [float("inf"), -float("inf"), 0])
        for message in itertools.islice(self._consumer, limit):
            reader = fastavro.reader(io.BytesIO(message.value()))
            alert = next(reader)  # raise StopIteration
            stats = topic_stats[message.topic()]
            if alert["candidate"]["jd"] < stats[0]:
                stats[0] = alert["candidate"]["jd"]
            if alert["candidate"]["jd"] > stats[1]:
                stats[1] = alert["candidate"]["jd"]
            stats[2] += 1
            if self.archive_updater:
                self.archive_updater.insert_alert(
                    alert,
                    reader.writer_schema,
                    message.partition(),
                    int(1e6 * time.time()),
                )
            yield io.BytesIO(message.value())
        log.info("Got messages from topics: {}".format(dict(topic_stats)))

    def __iter__(self) -> Iterator[io.IOBase]:
        return self.alerts()
