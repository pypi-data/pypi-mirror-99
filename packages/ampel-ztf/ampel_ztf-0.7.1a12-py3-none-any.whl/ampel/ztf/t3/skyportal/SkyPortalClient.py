#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-ZTF/ampel/ztf/t3/skyportal/SkyPortalClient.py
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 16.09.2020
# Last Modified Date: 16.09.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

import asyncio, base64, gzip, io, json, math, time, sys, aiohttp, backoff, pydantic.errors
import numpy as np

from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime
from astropy.io import fits
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from pydantic import AnyHttpUrl
if sys.version_info.minor > 8:
	from typing import TypedDict
else:
	from typing_extensions import TypedDict
from typing import Any, Dict, Generator, List, Optional, overload, Sequence, Set, TYPE_CHECKING, Union

from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.log.AmpelLogger import AmpelLogger
from ampel.metrics.AmpelMetricsRegistry import AmpelMetricsRegistry
from ampel.model.Secret import Secret
from ampel.protocol.LoggerProtocol import LoggerProtocol
from ampel.enum.T2RunState import T2RunState
from ampel.util.collections import ampel_iter

if TYPE_CHECKING:
    from pydantic import AnyUrl
    from pydantic.fields import ModelField
    from pydantic.main import BaseConfig

    from ampel.config.AmpelConfig import AmpelConfig
    from ampel.content.DataPoint import DataPoint
    from ampel.content.T2Document import T2Document
    from ampel.view.TransientView import TransientView


stat_http_errors = AmpelMetricsRegistry.counter(
    "http_request_errors",
    "HTTP request failures",
    subsystem=None,
    labelnames=("method", "endpoint"),
)
stat_http_responses = AmpelMetricsRegistry.counter(
    "http_responses",
    "HTTP responses successfully recieved",
    subsystem=None,
    labelnames=("method", "endpoint"),
)
stat_http_time = AmpelMetricsRegistry.histogram(
    "http_request_time",
    "Duration of HTTP requests",
    unit="seconds",
    subsystem=None,
    labelnames=("method", "endpoint"),
)
stat_concurrent_requests = AmpelMetricsRegistry.gauge(
    "http_requests_inprogress",
    "Number of HTTP requests in flight",
    subsystem=None,
    labelnames=("method", "endpoint"),
    multiprocess_mode="livesum",
)


def sanitize_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_json(v) for k, v in obj.items()}
    elif isinstance(obj, (tuple, list)):
        return [sanitize_json(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj


def encode_t2_body(t2: "T2Document") -> str:
    assert t2["body"] is not None
    doc = t2["body"][-1]
    return base64.b64encode(
        json.dumps(
            {
                "timestamp": datetime.fromtimestamp(doc["ts"]).isoformat(),
                **{k: sanitize_json(v) for k, v in doc.items() if k != "ts"},
            },
            default=lambda o: None,
        ).encode()
    ).decode()


def decode_t2_body(blob: str) -> Dict[str, Any]:
    doc = json.loads(base64.b64decode(blob.encode()).decode())
    return {"ts": int(datetime.fromisoformat(doc.pop("timestamp")).timestamp()), **doc}


def render_thumbnail(cutout_data: bytes) -> str:
    """
    Render gzipped FITS as base64-encoded PNG
    """
    with gzip.open(io.BytesIO(cutout_data), "rb") as f:
        with fits.open(f) as hdu:
            # header = hdu[0].header
            img = np.flipud(hdu[0].data)
    mask = np.isfinite(img)

    fig = Figure(figsize=(1, 1))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    ax.imshow(
        img,
        # clip pixel values below the median
        norm=Normalize(*np.percentile(img[mask], [0.5, 99.5])),
        aspect="auto",
        origin="lower",
    )

    with io.BytesIO() as buf:
        fig.savefig(buf, dpi=img.shape[0])
        return base64.b64encode(buf.getvalue()).decode()


ZTF_FILTERS = {1: "ztfg", 2: "ztfr", 3: "ztfi"}
CUTOUT_TYPES = {"science": "new", "template": "ref", "difference": "sub"}


class SkyPortalAPIError(IOError):
    ...


class UrlPathError(pydantic.errors.UrlError):
    code = "url.path"
    msg_template = "URL path must be empty, not {path!r}"

class BaseHttpUrl(AnyHttpUrl):
    """An http(s) URL with path unset"""

    @classmethod
    def validate(cls, value: Any, field: 'ModelField', config: 'BaseConfig') -> 'AnyUrl':
        url = super().validate(value, field, config)
        if url.path is not None:
            raise UrlPathError(path=url.path)
        return url
    # @classmethod
    # def validate_parts(cls, parts: Dict[str, str]) -> Dict[str, str]:
    #     parts["path"] = None
    #     return super().validate_parts(parts)


class SkyPortalClient(AmpelBaseModel):

    #: Base URL of SkyPortal server
    base_url: BaseHttpUrl
    #: API token
    token: Secret[str]
    #: Maximum number of in-flight requests
    max_parallel_connections: int = 1

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._request_kwargs = {
            "headers": {"Authorization": f"token {self.token.get()}"}
        }
        self._ids: Dict[str, Dict[str, int]] = {}
        self._session: Optional[aiohttp.ClientSession] = None
        self._semaphore: Optional[asyncio.Semaphore] = None

    @asynccontextmanager
    async def session(self, limit_per_host=0):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit_per_host=limit_per_host)
        ) as session:
            self._session = session
            self._semaphore = asyncio.Semaphore(self.max_parallel_connections)
            yield self
            self._session = None
            self._semaphore = None

    @overload
    async def request(
        self,
        verb: str,
        endpoint: str,
        raise_exc: bool,
        _decode_json: None,
        **kwargs: Dict[str, Any],
    ) -> aiohttp.ClientResponse:
        ...

    @overload
    async def request(
        self,
        verb: str,
        endpoint: str,
        raise_exc: bool,
        _decode_json: bool,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        ...

    @backoff.on_exception(
        backoff.expo,
        (
            aiohttp.ClientResponseError,
            aiohttp.ClientConnectionError,
            asyncio.TimeoutError,
        ),
        max_time=300,
    )
    async def request(
        self,
        verb: str,
        endpoint: str,
        raise_exc: bool = True,
        _decode_json: Optional[bool] = True,
        **kwargs: Dict[str, Any],
    ) -> Union[aiohttp.ClientResponse, Dict[str, Any]]:
        if self._session is None or self._semaphore is None:
            raise ValueError(
                "call operations within an `async with self.session()` block"
            )
        if endpoint.startswith("/"):
            url = self.base_url + endpoint
        else:
            url = self.base_url + "/api/" + endpoint
        labels = (verb, endpoint.split("/")[0])
        async with self._semaphore:
            with stat_http_time.labels(*labels).time(), stat_http_errors.labels(
                *labels
            ).count_exceptions(
                (
                    aiohttp.ClientResponseError,
                    aiohttp.ClientConnectionError,
                    asyncio.TimeoutError,
                )
            ), stat_concurrent_requests.labels(
                *labels
            ).track_inprogress():
                async with self._session.request(
                    verb, url, **{**self._request_kwargs, **kwargs}
                ) as response:
                    if response.status >= 500:
                        response.raise_for_status()
                    stat_http_responses.labels(*labels).inc()
                    if _decode_json:
                        payload = await response.json()
                        if raise_exc and payload["status"] != "success":
                            raise SkyPortalAPIError(payload["message"])
                        return payload
                    else:
                        return response

    async def get_id(self, endpoint, params, default=None):
        """Query for an object by id, inserting it if not found"""
        if not (response := await self.get(endpoint, params=params, raise_exc=False))[
            "data"
        ]:
            response = await self.post(endpoint, json=default or params)
        if isinstance(response["data"], list):
            return response["data"][0]["id"]
        else:
            return response["data"]["id"]

    async def get_by_name(self, endpoint, name):
        if endpoint not in self._ids:
            self._ids[endpoint] = {}
        if name not in self._ids[endpoint]:
            self._ids[endpoint][name] = await self._get_by_name(endpoint, name)
        return self._ids[endpoint][name]

    async def _get_by_name(self, endpoint, name):
        try:
            return next(
                d["id"]
                for d in (await self.get(endpoint, params={"name": name}))["data"]
                if d["name"] == name
            )
        except StopIteration:
            pass
        raise KeyError(f"No {endpoint} named {name}")

    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request("PUT", endpoint, **kwargs)

    async def head(self, endpoint: str, **kwargs) -> aiohttp.ClientResponse:
        return await self.request("HEAD", endpoint, _decode_json=None, **kwargs)


class FilterGroupProvisioner(SkyPortalClient):
    """
    Set up filters to corresponding to AMPEL channels
    """

    #: mapping from ampel stream name to Fritz stream name
    stream_names: Dict[str, str] = {
        "ztf_uw_public": "ZTF Public",
        "ztf_uw_private": "ZTF Public+Partnership",
        "ztf_uw_caltech": "ZTF Public+Partnership+Caltech",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def create_filter(self, name, stream, group):
        try:
            return await self.get_by_name("filters", name)
        except KeyError:
            ...
        doc = {
            "name": name,
            "stream_id": await self.get_by_name("streams", self.stream_names[stream]),
            "group_id": await self.get_by_name("groups", group),
        }
        await self.post("filters", json=doc)
        return await self.get_by_name("filters", name)

    async def create_filters(
        self, config: "AmpelConfig", group: str, stream: Optional[str] = None
    ) -> None:
        """
        Create a dummy SkyPortal filter for each Ampel filter
        
        :param group: name of group that should own the filter
        :param stream:
          name of the filter's alert stream (meaningless, since there is no
          filter actually defined)
        """
        for channel in config.get("channel", dict, raise_exc=True).values():
            if not channel.get("active", True):
                continue
            name = f"AMPEL.{channel['channel']}"
            try:
                await self.get_by_name("filters", name)
                continue
            except KeyError:
                ...
            await self.create_filter(name, stream or channel["template"], group)


async def provision_seed_data(client: SkyPortalClient):
    """Set up instruments and groups for a test instance"""
    p48 = await client.get_id(
        "telescope",
        {"name": "P48"},
        {
            "diameter": 1.2,
            "elevation": 1870.0,
            "lat": 33.3633675,
            "lon": -116.8361345,
            "nickname": "Palomar 1.2m Oschin",
            "name": "P48",
            "skycam_link": "http://bianca.palomar.caltech.edu/images/allsky/AllSkyCurrentImage.JPG",
            "robotic": True,
        },
    )

    source = {
        "instrument": client.get_id(
            "instrument",
            {"name": "ZTF"},
            {
                "filters": ["ztfg", "ztfr", "ztfi"],
                "type": "imager",
                "band": "optical",
                "telescope_id": p48,
                "name": "ZTF",
            },
        ),
        "stream": await client.get_id("streams", {"name": "ztf_partnership"}),
        "group": 1,  # root group
    }
    if not source["stream"] in [
        groupstream["id"]
        for groupstream in (await client.get(f"groups/{source['group']}"))["data"][
            "streams"
        ]
    ]:
        await client.post(
            f"groups/{source['group']}/streams", json={"stream_id": source["stream"]}
        )
    source["filter"] = await client.get_id(
        "filters",
        {"name": "highlander"},
        {
            "name": "highlander",
            "stream_id": source["stream"],
            "group_id": source["group"],
        },
    )

    # ensure that all users are in the root group
    users = [
        users["username"]
        for users in (await client.get(f"groups/{source['group']}"))["data"]["users"]
    ]
    for user in (await client.get("user"))["data"]:
        if not user["username"] in users:
            await client.post(
                f"groups/{source['group']}/users", json={"username": user["username"]},
            )

    return source


class PostReport(TypedDict):
    new: bool  #: is this a new source?
    candidates: List[int]  #: new candidates created
    save_error: Optional[str]  #: error raised while saving source
    photometry_count: int  #: size of posted photometry
    photometry_error: Optional[str]  #: error raised while posting photometry
    thumbnail_count: int  #: number of thumbnails posted
    comments: int  #: number of comments posted
    comment_errors: List[str]  #: errors raised while posting comments
    dt: float  #: elapsed time in seconds


class BaseSkyPortalPublisher(SkyPortalClient):

    logger: LoggerProtocol

    def __init__(self, **kwargs):
        if "logger" not in kwargs:
            kwargs["logger"] = AmpelLogger.get_logger()
        super().__init__(**kwargs)

    def _transform_datapoints(
        self, dps: Sequence["DataPoint"], after=-float("inf")
    ) -> Generator[Dict[str, Any], None, None]:
        for dp in dps:
            body = dp["body"]
            if body["jd"] <= after:
                continue
            if "SUPERSEDED" in dp["tag"]:
                continue
            base = {
                "_id": dp["_id"],
                "filter": ZTF_FILTERS[body["fid"]],
                "mjd": body["jd"] - 2400000.5,
                "limiting_mag": body["diffmaglim"],
            }
            if body.get("magpsf") is not None:
                content = {
                    "mag": body["magpsf"],
                    "magerr": body["sigmapsf"],
                    "ra": body["ra"],
                    "dec": body["dec"],
                }
            else:
                content = {k: None for k in ("mag", "magerr", "ra", "dec")}
            yield {**base, **content}

    def make_photometry(
        self, datapoints: Sequence["DataPoint"], after=-float("inf")
    ) -> Dict[str, Any]:
        content = defaultdict(list)
        for doc in self._transform_datapoints(datapoints, after):
            for k, v in doc.items():
                content[k].append(v)
        return dict(content)

    async def _find_instrument(self, tags: Sequence[Union[int, str]]) -> int:
        for tag in tags:
            try:
                return await self.get_by_name("instrument", tag)
            except Exception:
                ...
        raise KeyError(f"None of {tags} match a known instrument")

    async def post_candidate(
        self,
        view: "TransientView",
        filters: Optional[List[str]] = None,
        groups: Optional[List[str]] = None,
        instrument: Optional[str] = None,
    ) -> PostReport:
        """
        Perform the following actions:
          * Post candidate to filters specified by ``filters``. ``ra``/``dec``
            are taken from the most recent detection; ``drb`` from the maximum
            over detections.
          * Post photometry using the ``candid`` of the latest detection.
          * Post a PNG-encoded cutout of the last detection image.
          * Post each T2 result as comment with a JSON-encoded attachment. If
            a comment corresponding to the T2 unit already exists, overwrite it
            with the most recent result.
        
        :param view:
            Data to post
        :param filters:
            Names of the filter to associate with the candidate. If None, use
            filters named AMPEL.{channel} for each ``channel`` the transient
            belongs to.
        :param groups:
            Names of the groups to save the source to. If None, use all
            accessible groups associated with token.
        :param instrumentname:
            Name of the instrument with which to associate the photometry.
        """

        ret: PostReport = {
            "new": True,
            "candidates": [],
            "save_error": None,
            "photometry_count": 0,
            "photometry_error": None,
            "thumbnail_count": 0,
            "comments": 0,
            "comment_errors": [],
            "dt": -time.time(),
        }

        assert view.stock, f"{self.__class__} requires stock records"
        filter_ids = {
            name: await self.get_by_name("filters", name)
            for name in (
                filters
                or [f"AMPEL.{channel}" for channel in ampel_iter(view.stock["channel"])]
            )
        }
        group_ids = {await self.get_by_name("groups", name) for name in (groups or [])}
        assert view.stock["tag"] is not None
        instrument_id = (
            await self.get_by_name("instrument", instrument)
            if instrument
            else await self._find_instrument(view.stock["tag"])
        )

        assert view.stock and view.stock["name"] is not None
        name = next(
            n for n in view.stock["name"] if isinstance(n, str) and n.startswith("ZTF")
        )

        # all photometry, in time order
        assert view.t0 is not None
        dps = sorted(view.t0, key=lambda pp: pp["body"]["jd"])
        # detections, in time order
        pps = [pp for pp in dps if pp["_id"] > 0]

        # post transient
        candidate = {
            "ra": pps[-1]["body"]["ra"],
            "dec": pps[-1]["body"]["dec"],
            "ra_dis": pps[0]["body"]["ra"],
            "dec_dis": pps[0]["body"]["dec"],
            "origin": "Ampel",
            "score": max(drb)
            if (
                drb := [
                    rb
                    for pp in pps
                    if (rb := pp["body"].get("drb", pp["body"]["rb"])) is not None
                ]
            )
            else None,
            "detect_photometry_count": len(pps),
            "transient": True,  # sure, why not
        }
        new_filters = set(filter_ids.values())

        if (response := await self.get(f"candidates/{name}", raise_exc=False))[
            "status"
        ] == "success":
            # Only update filters, not the candidate itself
            new_filters.difference_update(response["data"]["filter_ids"])
            candidate = {}
            ret["new"] = False

        # Walk through the non-autocomplete journal entries in time order,
        # finding the time and alert id at which each filter passed for the
        # first time. If the candidate has not yet been posted, do so for the
        # first alert that passes a filter.
        for jentry in view.get_journal_entries(tier=0) or []:
            if jentry["extra"] is None or jentry["extra"].get("ac", False):
                continue
            # no more filters left to update
            if not new_filters:
                break
            # set all filters to passing on the first go if filters were
            # specified explicitly
            fids = (
                list(new_filters)
                if filters
                else [
                    fid
                    for channel in ampel_iter(jentry["channel"])
                    if (fid := filter_ids[f"AMPEL.{channel}"]) in new_filters
                ]
            )
            # no new filters passed on this alert
            if not fids:
                continue
            new_filters.difference_update(fids)
            candidate_ids = (
                await self.post(
                    "candidates",
                    json={
                        "id": name,
                        "filter_ids": fids,
                        "passing_alert_id": jentry["extra"]["alert"],
                        "passed_at": datetime.fromtimestamp(jentry["ts"]).isoformat(),
                        **candidate,
                    },
                )
            )["data"]["ids"]
            ret["candidates"] += candidate_ids
            candidate = {}

        # Save source to groups, if specified
        if groups:
            try:
                source = (await self.get(f"sources/{name}"))["data"]
                prev_groups = {group["id"] for group in source["groups"]}
            except SkyPortalAPIError:
                prev_groups = set()
            if groups_to_post := group_ids.difference(prev_groups):
                try:
                    await self.post(
                        "sources", json={"id": name, "group_ids": list(groups_to_post)}
                    )
                except SkyPortalAPIError as exc:
                    ret["save_error"] = exc.args[0]

        # Post photometry for the latest light curve.
        # For ZTF, the id of the most recent detection is the alert id
        # NB: we rely on the advertised, but as of 2020-09-17, unimplemented,
        # feature that repeated POST /api/photometry with the same alert_id and
        # group_ids are idempotent
        photometry = {
            "obj_id": name,
            "group_ids": "all",
            "magsys": "ab",
            "instrument_id": instrument_id,
            **self.make_photometry(dps),
        }
        datapoint_ids = photometry.pop("_id")
        try:
            photometry_response = await self.put("photometry", json=photometry)
            photometry_ids = photometry_response["data"]["ids"]
            assert len(datapoint_ids) == len(photometry_ids)
            ret["photometry_count"] = len(photometry_ids)
        except SkyPortalAPIError as exc:
            ret["photometry_error"] = exc.args[0]

        # SkyPortal only supports one of thumbnail per object and type
        # ('new', 'ref', 'sub', 'sdss', 'dr8', 'new_gz', 'ref_gz', 'sub_gz')
        # Post one of each type only if they do not yet exist.
        existing_cutouts: Set[str] = {
            t["type"] for t in response["data"]["thumbnails"]
        } if response["status"] == "success" else set()
        for candid, cutouts in (view.extra or {}).get("ZTFCutoutImages", {}).items():
            for kind, blob in (cutouts or {}).items():
                if CUTOUT_TYPES[kind] in existing_cutouts:
                    continue
                assert isinstance(blob, bytes)
                # FIXME: switch back to FITS when SkyPortal supports it
                await self.post(
                    "thumbnail",
                    json={
                        "obj_id": name,
                        "data": render_thumbnail(blob),
                        "ttype": CUTOUT_TYPES[kind],
                    },
                    raise_exc=True,
                )
                existing_cutouts.add(CUTOUT_TYPES[kind])
                ret["thumbnail_count"] += 1

        # represent latest T2 results as a comments
        latest_t2: Dict[str, "T2Document"] = {}
        for t2 in view.t2 or []:
            if t2["status"] != T2RunState.COMPLETED or not t2["body"]:
                continue
            assert isinstance(t2["unit"], str)
            if t2["unit"] not in latest_t2 or latest_t2[t2["unit"]]["_id"] < t2["_id"]:
                latest_t2[t2["unit"]] = t2
        previous_comments = (
            response["data"]["comments"] if response["status"] == "success" else []
        )

        for t2 in latest_t2.values():
            # find associated comment
            for comment in previous_comments:
                if comment["text"] == t2["unit"]:
                    break
            else:
                # post new comment
                self.logger.debug(f"posting {t2['unit']}")
                try:
                    await self.post(
                        "comment",
                        json={
                            "obj_id": name,
                            "text": t2["unit"],
                            "attachment": {
                                "body": encode_t2_body(t2),
                                "name": f"{name}-{t2['unit']}.json",
                            },
                        },
                    )
                    ret["comments"] += 1
                except SkyPortalAPIError as exc:
                    ret["comment_errors"].append(exc.args[0])
                continue
            # update previous comment
            previous_body = decode_t2_body(comment["attachment_bytes"])
            if (t2["body"] is not None) and (
                t2["body"][-1]["ts"] > previous_body["ts"]
            ):
                self.logger.debug(f"updating {t2['unit']}")
                try:
                    await self.put(
                        f"comment/{comment['id']}",
                        json={
                            "attachment_bytes": encode_t2_body(t2),
                            "author_id": comment["author_id"],
                            "obj_id": name,
                            "text": comment["text"],
                        },
                    )
                    ret["comments"] += 1
                except SkyPortalAPIError as exc:
                    ret["comment_errors"].append(exc.args[0])
            else:
                self.logger.debug(f"{t2['unit']} exists and is current")

        ret["dt"] += time.time()

        return ret
