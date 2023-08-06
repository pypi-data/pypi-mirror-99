# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from asyncio import Future, sleep
from collections import defaultdict
from typing import Awaitable, Collection, Dict, List, Optional, Union, cast
import warnings

from ..client._reader_match import is_match
from ..damlast.daml_lf_1 import TypeConName
from ..damlast.protocols import SymbolLookup
from ..model.core import (
    ContractContextualData,
    ContractContextualDataCollection,
    ContractId,
    ContractMatch,
    ContractsState,
    UnknownTemplateWarning,
)
from ..model.reading import ContractArchiveEvent, ContractCreateEvent
from ..scheduler import Invoker
from ..util.asyncio_util import await_then


class ActiveContractSet:
    def __init__(self, invoker: "Invoker", lookup: "SymbolLookup"):
        self.invoker = invoker
        self.lookup = lookup
        self._tcdata = defaultdict(
            TemplateContractData
        )  # type: Dict[TypeConName, TemplateContractData]

    def handle_create(self, event: ContractCreateEvent) -> None:
        self._tcdata[event.cid.value_type].handle_create(event)

    def handle_archive(self, event: ContractArchiveEvent) -> None:
        self._tcdata[event.cid.value_type].handle_archive(event)

    def get(self, cid: "Union[str, ContractId]") -> "Optional[ContractContextualData]":
        """
        Return information for the associated :class:`ContractId`.

        :param cid: Either a ContractId or a string that represents a ContractId.
        :return: Contract information for the specified contract ID.
        """
        tcd = self._tcdata.get(cid.value_type) if isinstance(cid, ContractId) else None
        if tcd is not None:
            return tcd.get(cid)
        else:
            # untyped ContractId lookup, so scan across all templates
            for tcd in self._tcdata.values():
                cxd = tcd.get(cid)
                if cxd is not None:
                    return cxd
            return None

    def read_active(self, template_name: str, match: ContractMatch = None) -> ContractsState:
        return {cxd.cid: cxd.cdata for cxd in self.read_full(template_name, match)}

    def read_full(
        self, template_name: str, match: ContractMatch = None, include_archived: bool = False
    ) -> ContractContextualDataCollection:
        unfiltered = self._get_template_state(template_name)
        all_items = [
            item for tcd in unfiltered.values() for item in tcd.subset(match, include_archived)
        ]
        return ContractContextualDataCollection(all_items)

    async def read_async(
        self, template_name: str, match: ContractMatch = None, min_count: int = 1
    ) -> "ContractsState":
        from .. import LOG

        # Fetch matching names; we may need to wait for a package to be fetched in order to do this.
        # Note that this loop may never terminate; in this case, this behavior is actually
        # acceptable because it is what enables us to wait indefinitely for the creation of a
        # contract of a specific type. Because we need type information available to parse data
        # from the read stream, by the time data ends up in the ACS, the lookup will definitely
        # know of the template name.
        names = []
        fail_count = 0
        while not names:
            names = self.lookup.template_names(template_name)
            if not names:
                fail_count += 1
                await sleep(1)

                if fail_count % 15 == 0:
                    LOG.warning(
                        "ACS read_async(%r) is still waiting for a package that contains that "
                        "template. If this is taking longer than you expect, it might be because "
                        "the relevant package is not loaded on your ledger.",
                        template_name,
                    )

        unfiltered = self._get_template_state(template_name)
        if len(unfiltered) > 1:
            warnings.warn(
                "Wildcard searches are not supported on async ACS queries",
                UnknownTemplateWarning,
                stacklevel=3,
            )
            unfiltered = dict()  # type: Dict[TypeConName, TemplateContractData]

        ((tt, tcd),) = unfiltered.items()

        query = PendingQuery(self.invoker, match, min_count)
        # if the current state is already a match, then don't remember the query since we're
        # already done
        if tcd is None or not query.check_ready(tcd):
            tcd.register_query(query)

        return await await_then(query.future, lambda cxds: {cxd.cid: cxd.cdata for cxd in cxds})

    def _get_template_state(self, template_name: str) -> "Dict[TypeConName, TemplateContractData]":
        names = self.lookup.template_names(template_name)
        if not names:
            warnings.warn(
                f"Unknown template name: {template_name}", UnknownTemplateWarning, stacklevel=4
            )

        return {name: self._tcdata[name] for name in names}


class TemplateContractData:
    """
    Storage for state related to a specific :class:`Template`.
    """

    def __init__(self):
        # raw ContractId to ContractContextualData
        self._data = dict()  # type: Dict[str, ContractContextualData]
        # outstanding ACS queries
        self._queries = list()  # type: List[PendingQuery]

    def handle_create(self, event: ContractCreateEvent) -> None:
        self._data[event.cid.value] = ContractContextualData(
            cid=event.cid, cdata=event.cdata, effective_at=event.time, archived_at=None, active=True
        )

        self._queries = [q for q in self._queries if not q.check_ready(self)]

    def handle_archive(self, event: ContractArchiveEvent) -> None:
        existing_data = self._data.get(event.cid.value)
        effective_at = existing_data.effective_at if existing_data is not None else None
        self._data[event.cid.value] = ContractContextualData(
            cid=event.cid,
            cdata=None,
            effective_at=effective_at,
            archived_at=event.time,
            active=False,
        )

    def get(self, cid: "Union[str, ContractId]") -> "Optional[ContractContextualData]":
        if isinstance(cid, ContractId):
            cid = cid.value
        return self._data.get(cid)

    def subset(
        self, match: "ContractMatch", include_archived: bool
    ) -> "Collection[ContractContextualData]":
        return [
            cxd
            for cxd in self._data.values()
            if (include_archived or cxd.active) and is_match(match, cxd.cdata)
        ]

    def register_query(self, query: "PendingQuery") -> None:
        self._queries.append(query)


class PendingQuery:
    def __init__(self, invoker: "Invoker", match, min_count: int):
        self.future = invoker.create_future()  # type: Awaitable[Collection[ContractContextualData]]
        self.match = match
        self.min_count = min_count

    def check_ready(self, tcd: "TemplateContractData") -> bool:
        matches = tcd.subset(self.match, False)
        if len(matches) >= self.min_count:
            cast(Future, self.future).set_result(matches)
            return True
        else:
            return False
