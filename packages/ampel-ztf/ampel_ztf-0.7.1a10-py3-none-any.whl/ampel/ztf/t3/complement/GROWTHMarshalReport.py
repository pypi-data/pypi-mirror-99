#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/contrib/hu/t3/complement/GROWTHMarshalReport.py
# License           : BSD-3-Clause
# Author            : Jakob van Santen <jakob.van.santen@desy.de>
# Date              : 03.11.2020
# Date              : 03.11.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

from typing import Any, Dict, Optional, Sequence, Iterable

import backoff
import requests

from ampel.type import StockId
from ampel.core.AmpelBuffer import AmpelBuffer
from ampel.t3.complement.AbsT3DataAppender import AbsT3DataAppender
from ampel.ztf.base.CatalogMatchUnit import CatalogMatchAdminUnit


class GROWTHMarshalReport(CatalogMatchAdminUnit, AbsT3DataAppender):
    """
    Add GROWTH Marshal records from a local extcats mirror of the ProgramList.
    Though the GROWTH Marshal is no longer being updated, this is useful for
    looking up classifications of sources first discovered with ZTF I.
    """

    def complement(self, records: Iterable[AmpelBuffer]) -> None:
        for record in records:

            if (stock := record.get("stock", None)) is None:
                raise ValueError(f"{self.__class__.__name__} requires stock records")

            report = self.get_catalog_item(stock.get("name") or tuple())
            if record.get("extra") is None or record["extra"] is None:
                record["extra"] = {self.__class__.__name__: report}
            else:
                record["extra"][self.__class__.__name__] = report

    @backoff.on_exception(
        backoff.expo,
        requests.HTTPError,
        giveup=lambda e: e.response.status_code not in {503, 429},
        max_time=60,
    )
    def _lookup(self, name) -> Optional[Dict[str, Any]]:
        response = self.session.get(f"catalogs/GROWTHMarshal/{name}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def get_catalog_item(self, names: Sequence[StockId]) -> Optional[Dict[str, Any]]:
        """Get catalog entry associated with the stock name"""
        for name in names:
            if (
                isinstance(name, str)
                and name.startswith("ZTF")
                and (entry := self._lookup(name))
            ):
                return entry
        return None
