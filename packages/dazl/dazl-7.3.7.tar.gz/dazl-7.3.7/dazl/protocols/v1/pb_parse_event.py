# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Conversion methods from Ledger API Protobuf-generated types to dazl/Pythonic types.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union
import warnings

from ... import LOG
from ..._gen.com.daml.ledger.api.v1 import (
    active_contracts_service_pb2 as acs_pb2,
    event_pb2,
    ledger_offset_pb2 as lo_pb2,
    transaction_filter_pb2 as txf_pb2,
    transaction_pb2 as tx_pb2,
    transaction_service_pb2 as txs_pb2,
    value_pb2,
)
from ...damlast.daml_lf_1 import DottedName, ModuleRef, PackageRef, TypeConName
from ...damlast.daml_types import con
from ...damlast.lookup import find_choice
from ...damlast.protocols import SymbolLookup
from ...model.reading import (
    ActiveContractSetEvent,
    BaseEvent,
    ContractArchiveEvent,
    ContractCreateEvent,
    ContractExercisedEvent,
    ContractFilter,
    OffsetEvent,
    TransactionEndEvent,
    TransactionFilter,
    TransactionStartEvent,
)
from ...prim import Party, to_datetime
from ...values import Context, ProtobufDecoder

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from ...model.types_store import PackageStore


DECODER = ProtobufDecoder()


@dataclass(frozen=True)
class BaseEventDeserializationContext:
    """
    Attributes required throughout the deserialization of an event stream.
    """

    client: "Any"
    lookup: "SymbolLookup"
    store: "PackageStore"
    party: "Party"
    ledger_id: str

    def deserializer_context(self) -> "Context":
        return Context(DECODER, self.lookup)

    def offset_event(self, time: datetime, offset: str) -> OffsetEvent:
        return OffsetEvent(
            self.client, self.party, time, self.ledger_id, self.lookup, self.store, offset
        )

    def active_contract_set(
        self, offset: str, workflow_id: str
    ) -> "ActiveContractSetEventDeserializationContext":
        return ActiveContractSetEventDeserializationContext(
            self.client, self.lookup, self.store, self.party, self.ledger_id, offset, workflow_id
        )

    def transaction(
        self, time: datetime, offset: str, command_id: str, workflow_id: str
    ) -> "TransactionEventDeserializationContext":
        return TransactionEventDeserializationContext(
            self.client,
            self.lookup,
            self.store,
            self.party,
            self.ledger_id,
            time,
            offset,
            command_id,
            workflow_id,
        )


@dataclass(frozen=True)
class ActiveContractSetEventDeserializationContext(BaseEventDeserializationContext):
    """
    Attributes required throughout the deserialization of the Active Contract Set.
    """

    offset: str
    workflow_id: str

    def active_contract_set_event(
        self, contract_events: "Sequence[ContractCreateEvent]"
    ) -> "ActiveContractSetEvent":
        return ActiveContractSetEvent(
            self.client,
            self.party,
            None,
            self.ledger_id,
            self.lookup,
            self.store,
            self.offset,
            contract_events,
        )

    def contract_created_event(self, cid, cdata, event_id, witness_parties) -> ContractCreateEvent:
        return ContractCreateEvent(
            client=self.client,
            party=self.party,
            time=None,
            ledger_id=self.ledger_id,
            lookup=self.lookup,
            package_store=self.store,
            offset=self.offset,
            command_id="",
            workflow_id=self.workflow_id,
            cid=cid,
            cdata=cdata,
            event_id=event_id,
            witness_parties=witness_parties,
        )


@dataclass(frozen=True)
class TransactionEventDeserializationContext(BaseEventDeserializationContext):
    """
    Attributes required throughout the deserialization of an event stream.
    """

    time: datetime
    offset: str
    command_id: str
    workflow_id: str

    def transaction_start_event(self, contract_events) -> TransactionStartEvent:
        return TransactionStartEvent(
            self.client,
            self.party,
            self.time,
            self.ledger_id,
            self.lookup,
            self.store,
            self.offset,
            self.command_id,
            self.workflow_id,
            contract_events,
        )

    def transaction_end_event(self, contract_events) -> TransactionEndEvent:
        return TransactionEndEvent(
            self.client,
            self.party,
            self.time,
            self.ledger_id,
            self.lookup,
            self.store,
            self.offset,
            self.command_id,
            self.workflow_id,
            contract_events,
        )

    def contract_created_event(self, cid, cdata, event_id, witness_parties) -> ContractCreateEvent:
        return ContractCreateEvent(
            client=self.client,
            party=self.party,
            time=self.time,
            ledger_id=self.ledger_id,
            package_store=self.store,
            lookup=self.lookup,
            offset=self.offset,
            command_id=self.command_id,
            workflow_id=self.workflow_id,
            cid=cid,
            cdata=cdata,
            event_id=event_id,
            witness_parties=witness_parties,
        )

    def contract_exercised_event(
        self,
        cid,
        cdata,
        event_id,
        witness_parties,
        contract_creating_event_id: str,
        choice: str,
        choice_argument: Any,
        acting_parties,
        consuming,
        child_event_ids,
        exercise_result,
    ) -> ContractExercisedEvent:
        return ContractExercisedEvent(
            client=self.client,
            party=self.party,
            time=self.time,
            ledger_id=self.ledger_id,
            package_store=self.store,
            lookup=self.lookup,
            offset=self.offset,
            command_id=self.command_id,
            workflow_id=self.workflow_id,
            cid=cid,
            cdata=cdata,
            event_id=event_id,
            witness_parties=witness_parties,
            contract_creating_event_id=contract_creating_event_id,
            acting_parties=acting_parties,
            choice=choice,
            choice_args=choice_argument,
            consuming=consuming,
            child_event_ids=child_event_ids,
            exercise_result=exercise_result,
        )

    def contract_archived_event(
        self, cid, cdata, event_id, witness_parties
    ) -> ContractArchiveEvent:
        return ContractArchiveEvent(
            client=self.client,
            party=self.party,
            time=self.time,
            ledger_id=self.ledger_id,
            package_store=self.store,
            lookup=self.lookup,
            offset=self.offset,
            command_id=self.command_id,
            workflow_id=self.workflow_id,
            cid=cid,
            cdata=cdata,
            event_id=event_id,
            witness_parties=witness_parties,
        )


def serialize_transactions_request(
    f: "TransactionFilter", ledger_id: str, party: str
) -> "txs_pb2.GetTransactionsRequest":
    if f.current_offset is not None:
        ledger_offset = lo_pb2.LedgerOffset()
        ledger_offset.absolute = f.current_offset
    else:
        ledger_offset = lo_pb2.LedgerOffset()
        ledger_offset.boundary = 0

    if f.destination_offset is not None:
        final_offset = lo_pb2.LedgerOffset()
        final_offset.absolute = f.destination_offset
    else:
        final_offset = lo_pb2.LedgerOffset()
        final_offset.boundary = 1

    return txs_pb2.GetTransactionsRequest(
        ledger_id=ledger_id,
        begin=ledger_offset,
        end=final_offset,
        filter=serialize_transaction_filter(f, party),
    )


def serialize_acs_request(
    f: "ContractFilter", ledger_id: str, party: str
) -> "acs_pb2.GetActiveContractsRequest":
    return acs_pb2.GetActiveContractsRequest(
        ledger_id=ledger_id, filter=serialize_transaction_filter(f, party)
    )


def serialize_event_id_request(
    ledger_id: str, event_id: str, requesting_parties: "Sequence[str]"
) -> "txs_pb2.GetTransactionByEventIdRequest":
    return txs_pb2.GetTransactionByEventIdRequest(
        ledger_id=ledger_id, event_id=event_id, requesting_parties=requesting_parties
    )


def serialize_transaction_filter(
    contract_filter: "ContractFilter", party: str
) -> "txf_pb2.TransactionFilter":
    from .pb_ser_command import as_identifier

    identifiers = (
        [as_identifier(tt) for tt in contract_filter.templates]
        if contract_filter.templates is not None
        else None
    )

    parties = [party]
    if contract_filter.party_groups is not None:
        parties.extend(contract_filter.party_groups)

    filters_by_party = {}
    for party in parties:
        if identifiers is not None:
            filters_by_party[party] = txf_pb2.Filters(
                inclusive=txf_pb2.InclusiveFilters(template_ids=identifiers)
            )
        else:
            filters_by_party[party] = txf_pb2.Filters()

    return txf_pb2.TransactionFilter(filters_by_party=filters_by_party)


def to_transaction_events(
    context: "BaseEventDeserializationContext",
    tx_stream_pb: "Iterable[txs_pb2.GetTransactionsResponse]",
    tt_stream_pb: "Optional[Iterable[txs_pb2.GetTransactionTreesResponse]]",
    last_offset_override: "Optional[str]",
) -> "Sequence[BaseEvent]":
    """
    Convert a stream of :class:`GetTransactionsResponse` into a sequence of events.

    :param context:
        Additional data required for deserializing wire information into easily-consumable
        application events.
    :param tx_stream_pb:
        A stream of :class:`GetTransactionsResponse`.
    :param tt_stream_pb:
        An optional stream of :class:`GetTransactionTreesResponse`, used to enrich the stream with
        exercise events. Transactions included in this message that are _not_ in ``tx_stream_pb``
        will be discarded.
    :param last_offset_override:
        An optional last offset, that, if specified AND different from the last offset of the
        stream, causes a synthetic :class:`OffsetEvent` to be created at the end.
    :return:
    """
    events = []  # type: List[OffsetEvent]

    events_by_offset = dict()  # type: Dict[str, List[OffsetEvent]]
    for item_pb in tx_stream_pb:
        for transaction_pb in item_pb.transactions:
            events_by_offset[transaction_pb.offset] = list(
                to_transaction_chunk(context, transaction_pb)
            )

    if tt_stream_pb is not None:
        for transaction_tree_pb in tt_stream_pb:
            for transaction_pb in transaction_tree_pb.transactions:
                tx_events = events_by_offset.get(transaction_pb.offset)
                if tx_events is not None:
                    tx_events[-1:-1] = from_transaction_tree(context, transaction_pb)

    for tx_events in events_by_offset.values():
        events.extend(tx_events)

    if last_offset_override is not None:
        last_time = None if not events else events[-1].time
        last_offset = None if not events else events[-1].offset
        if last_offset != last_offset_override:
            events.append(context.offset_event(last_time, last_offset_override))

    return events


def to_acs_events(
    context: "BaseEventDeserializationContext", acs_stream_pb: "Iterable[Any]"
) -> "Sequence[ActiveContractSetEvent]":
    return [
        acs_evt
        for acs_response_pb in acs_stream_pb
        for acs_evt in to_acs_event(context, acs_response_pb)
    ]


def from_transaction_tree(
    context: "BaseEventDeserializationContext", tt_pb: "tx_pb2.TransactionTree"
) -> "Sequence[OffsetEvent]":
    t_context = context.transaction(
        time=to_datetime(tt_pb.effective_at),
        offset=tt_pb.offset,
        command_id=tt_pb.command_id,
        workflow_id=tt_pb.workflow_id,
    )

    events = []
    for evt_pb in tt_pb.events_by_id.values():
        evt = to_event(t_context, evt_pb)
        if isinstance(evt, ContractExercisedEvent):
            events.append(evt)

    return events


def to_acs_event(
    context: "BaseEventDeserializationContext", acs_pb: "acs_pb2.GetActiveContractsResponse"
):
    acs_context = context.active_contract_set(acs_pb.offset, acs_pb.workflow_id)
    contract_events = [
        evt
        for evt in (to_created_event(acs_context, evt_pb) for evt_pb in acs_pb.active_contracts)
        if evt is not None
    ]
    return [acs_context.active_contract_set_event(contract_events)]


def to_transaction_chunk(
    context: "BaseEventDeserializationContext", tx_pb: "tx_pb2.Transaction"
) -> "Sequence[OffsetEvent]":
    """
    Return a sequence of events parsed from a Ledger API ``Transaction`` protobuf message.

    :param context:
        Additional information taken from the enclosing message.
    :param tx_pb:
        The Ledger API ``Transaction`` to parse.
    :return:
        A :class:`TransactionStartEvent`, followed by zero or more :class:`ContractCreateEvent`
        and/or :class:`ContractArchiveEvent`, followed by :class:`TransactionEndEvent`.
    """

    t_context = context.transaction(
        time=to_datetime(tx_pb.effective_at),
        offset=tx_pb.offset,
        command_id=tx_pb.command_id,
        workflow_id=tx_pb.workflow_id,
    )

    contract_events = [to_event(t_context, evt_pb) for evt_pb in tx_pb.events]
    contract_events = [evt for evt in contract_events if evt is not None]

    return [
        t_context.transaction_start_event(contract_events),
        *contract_events,
        t_context.transaction_end_event(contract_events),
    ]


def to_event(
    context: "Union[TransactionEventDeserializationContext, ActiveContractSetEventDeserializationContext]",
    evt_pb: "event_pb2.Event",
) -> "Optional[BaseEvent]":
    try:
        event_type = evt_pb.WhichOneof("event")
    except ValueError:
        try:
            event_type = evt_pb.WhichOneof("kind")
        except ValueError:
            LOG.error("Deserialization error into an event of %r", evt_pb)
            raise

    if "created" == event_type:
        return to_created_event(context, evt_pb.created)
    elif "exercised" == event_type:
        return to_exercised_event(context, evt_pb.exercised)
    elif "archived" == event_type:
        return to_archived_event(context, evt_pb.archived)
    else:
        raise ValueError(f"unknown event type: {event_type}")


def to_created_event(
    context: "Union[TransactionEventDeserializationContext, ActiveContractSetEventDeserializationContext]",
    cr: "event_pb2.CreatedEvent",
) -> "Optional[ContractCreateEvent]":
    tt = con(to_type_con_name(cr.template_id))

    ctx = context.deserializer_context()
    cid = ctx.convert_contract_id(tt, cr.contract_id)
    cdata = ctx.convert(tt, cr.create_arguments)
    event_id = cr.event_id
    witness_parties = tuple(cr.witness_parties)

    return context.contract_created_event(cid, cdata, event_id, witness_parties)


def to_exercised_event(
    context: "TransactionEventDeserializationContext", er: "event_pb2.ExercisedEvent"
) -> "Optional[ContractExercisedEvent]":
    name = to_type_con_name(er.template_id)
    tt = con(name)

    template = context.lookup.template(name)
    choice = find_choice(template, er.choice)

    ctx = context.deserializer_context()

    cid = ctx.convert_contract_id(tt, er.contract_id)
    event_id = er.event_id
    witness_parties = tuple(er.witness_parties)
    try:
        contract_creating_event_id = er.contract_creating_event_id
    except AttributeError:
        contract_creating_event_id = None
    choice_args = ctx.convert(choice.arg_binder.type, er.choice_argument)
    acting_parties = tuple(er.acting_parties)
    consuming = er.consuming
    child_event_ids = er.child_event_ids
    exercise_result = ctx.convert(choice.ret_type, er.exercise_result)

    return context.contract_exercised_event(
        cid,
        None,
        event_id,
        witness_parties,
        contract_creating_event_id,
        er.choice,
        choice_args,
        acting_parties,
        consuming,
        child_event_ids,
        exercise_result,
    )


def to_archived_event(
    context: "TransactionEventDeserializationContext", ar: "event_pb2.ArchivedEvent"
) -> "Optional[ContractArchiveEvent]":
    tt = con(to_type_con_name(ar.template_id))
    event_id = ar.event_id
    witness_parties = tuple(ar.witness_parties)

    ctx = context.deserializer_context()
    cid = ctx.convert_contract_id(tt, ar.contract_id)
    return context.contract_archived_event(cid, None, event_id, witness_parties)


def to_type_con_name(identifier: "value_pb2.Identifier") -> "TypeConName":
    return TypeConName(
        ModuleRef(PackageRef(identifier.package_id), DottedName(identifier.module_name.split("."))),
        DottedName(identifier.entity_name.split(".")).segments,
    )
