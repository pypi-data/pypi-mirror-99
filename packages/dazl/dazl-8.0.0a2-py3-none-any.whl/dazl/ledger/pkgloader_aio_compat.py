# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Backwards compatibility symbols in support of the to-be-removed dazl.client.pkg_loader module.
This file is here in order to avoid import cycles.
"""

from asyncio import get_event_loop
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import timedelta
from typing import AbstractSet, Protocol
import warnings

from ..damlast.daml_lf_1 import PackageRef
from ..damlast.lookup import MultiPackageLookup
from .pkgloader_aio import DEFAULT_TIMEOUT, PackageLoader as NewPackageLoader

__all__ = ["SyncPackageService", "PackageLoader"]


class SyncPackageService(Protocol):
    """
    A service that synchronously provides package information.

    This _synchronous_ protocol was used in support of the _asynchronous_ PackageLoader for v7;
    this mismatch is a little confusing, so this API is deprecated.
    """

    def __init__(self):
        warnings.warn(
            "SyncPackageService is deprecated; implement the PackageService protocol instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    def package_bytes(self, package_id: "PackageRef") -> bytes:
        raise NotImplementedError("SyncPackageService.package_bytes requires an implementation")

    def package_ids(self) -> "AbstractSet[PackageRef]":
        raise NotImplementedError("SyncPackageService.package_ids requires an implementation")


class PackageLoader(NewPackageLoader):
    """
    Backwards-compatibility shim for dazl.client.pkg_loader.PackageLoader that exposes the same
    historical API but also emits a deprecation warning on construction.

    This shim will be removed in v9.
    """

    def __init__(
        self,
        package_lookup: "MultiPackageLookup",
        conn: "SyncPackageService" = None,
        timeout: "timedelta" = DEFAULT_TIMEOUT,
    ):
        warnings.warn(
            "dazl.client.pkg_loader.PackageLoader has moved to "
            "dazl.protocols.pkgloader_aio.PackageLoader and now requires an async package loader.",
            DeprecationWarning,
            stacklevel=2,
        )
        executor = ThreadPoolExecutor(3)
        super().__init__(package_lookup, PackageServiceWrapper(conn, executor), timeout, executor)


class PackageServiceWrapper:
    def __init__(self, impl: "SyncPackageService", executor: "ThreadPoolExecutor"):
        self.impl = impl
        self.executor = executor

    async def get_package(self, package_id: "PackageRef") -> bytes:
        loop = get_event_loop()
        return await loop.run_in_executor(self.executor, self.impl.package_bytes, package_id)

    async def list_package_ids(self) -> "AbstractSet[PackageRef]":
        loop = get_event_loop()
        return await loop.run_in_executor(self.executor, self.impl.package_ids)
