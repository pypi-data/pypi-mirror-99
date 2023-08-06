# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
:mod:`dazl.model` package
=========================

The :mod:`dazl.model` module is the low-level domain model for the Ledger. Most of the time, these
classes will not be instantiated directly, but will frequently be passed to your code to work with.

The most important classes:

:mod:`dazl.model.core`:
    :class:`~dazl.model.core.ContractId`

:mod:`dazl.model.writing`:
    Subclasses of :class:`~dazl.model.writing.Command` for the Write API:
    :class:`~dazl.model.writing.CreateCommand` and
    :class:`~dazl.model.writing.ExerciseCommand`

:mod:`dazl.model.types`:
    Type description classes:
    Subclasses of :class:`~dazl.model.types.Type`:
    :class:`~dazl.model.types.ScalarType`,
    :class:`~dazl.model.types.ListType`,
    :class:`~dazl.model.types.RecordType`,
    :class:`~dazl.model.types.VariantType`

.. automodule:: dazl.model.core
.. automodule:: dazl.model.ledger
.. automodule:: dazl.model.reading
.. automodule:: dazl.model.types
.. automodule:: dazl.model.types_store
.. automodule:: dazl.model.writing

"""

from . import core, ledger, network, reading, types, writing
