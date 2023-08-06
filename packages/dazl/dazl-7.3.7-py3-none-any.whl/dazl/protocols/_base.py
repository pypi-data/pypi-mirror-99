# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains the abstract base class that defines the protocol for interacting with a
process that implements the Ledger API.
"""
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Sequence, Union

from .. import LOG
from ..damlast.protocols import SymbolLookup
from ..model.ledger import LedgerMetadata
from ..model.network import HTTPConnectionSettings
from ..model.reading import BaseEvent, ContractFilter, TransactionFilter
from ..model.writing import CommandPayload
from ..prim import Party
from ..scheduler import Invoker
from ..util.typing import safe_cast, safe_optional_cast


@dataclass(frozen=True)
class LedgerConnectionOptions:
    lookup: "SymbolLookup"
    connect_timeout: "Optional[timedelta]"
    package_lookup_timeout: "Optional[timedelta]"
    eager_package_fetch: bool


class LedgerNetwork:
    """
    Abstract base class for creating connections to the ledger.
    """

    async def connect(
        self,
        party: "Union[str, Party]",
        settings: HTTPConnectionSettings,
        context_path: "Optional[str]",
    ) -> "LedgerClient":
        """
        Establish a connection to a Party.
        """
        raise NotImplementedError("connect must be implemented")

    async def connect_anonymous(
        self, settings: "HTTPConnectionSettings", context_path: "Optional[str]"
    ) -> None:
        """
        Establish a single no-Party connection (but only if no other connections have already been
        established). This is used by specialized setups that do not require Parties to be supplied
        for any reason (such as fetching initial ledger metadata).
        """

    async def ledger(self) -> "LedgerMetadata":
        """
        Return information about the entire ledger.
        """
        raise NotImplementedError("ledger must be implemented")

    async def sync_time(self) -> None:
        """
        Ensure that the local notion of time is in sync with the remote server. This method is only
        relevant for static-time implementations on the REST-based API, as the gRPC API pushes time
        updates through the TimeService. In these contexts, this method is a no-op.
        """

    async def upload_package(self, dar_contents: bytes) -> None:
        """
        Upload a DAR file to the ledger.

        :param dar_contents: The raw bytes that represent a package.
        """

    async def close(self):
        """
        Shut down all connections and transition the pool to the closed state.
        """

    @property
    def closed(self) -> bool:
        """
        Determine whether the underlying network connections to the LedgerNetwork are closed. This
        property should start as ``False`` when the pool is constructed, and ``True`` some time
        after ``close()`` is called.
        """
        raise NotImplementedError("closed must be implemented")


class LedgerClient:
    """
    Abstract base class that defines the required methods to define a protocol over the Ledger API.
    """

    async def commands(self, command_payload: "CommandPayload") -> None:
        """
        Submit a command to the ledger.

        The coroutine returns when the implementation has accepted the command for processing, but
        not necessarily committed to the ledger.

        :param command_payload: Payload of data to submit asynchronously.
        """
        raise NotImplementedError("commands must be implemented")

    async def active_contracts(self, contract_filter: "ContractFilter") -> "Sequence[BaseEvent]":
        """
        Return the current active contract set.
        """
        raise NotImplementedError("active contract set fetch must be implemented")

    async def events(self, transaction_filter: "TransactionFilter") -> "Sequence[BaseEvent]":
        """
        Return events from a certain offset in the ledger. The number of blocks
        returned is implementation-defined.
        """
        raise NotImplementedError("events must be implemented")

    async def events_end(self) -> str:
        """
        Return the (current) last offset of the ledger.
        """


class _LedgerConnection:
    def __init__(
        self,
        invoker: "Invoker",
        options: "LedgerConnectionOptions",
        settings: HTTPConnectionSettings,
        context_path: Optional[str],
    ):
        LOG.debug("Creating a gRPC channel for %s...", settings)
        import threading

        self.invoker = safe_cast(Invoker, invoker)
        self.options = safe_cast(LedgerConnectionOptions, options)
        self.settings = safe_cast(HTTPConnectionSettings, settings)
        self.context_path = safe_optional_cast(str, context_path)
        self.close_evt = threading.Event()

    def close(self):
        self.close_evt.set()
