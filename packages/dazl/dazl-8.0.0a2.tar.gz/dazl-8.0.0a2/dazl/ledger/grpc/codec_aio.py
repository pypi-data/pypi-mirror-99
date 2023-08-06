# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
This module contains the mapping between Protobuf objects and Python/dazl types.
"""

# Earlier versions of dazl (before v8) had an API that mapped less directly to the gRPC Ledger API.
# But with the HTTP JSON API, many common ledger methods now have much more direct translations that
# still manage to adhere quite closely to dazl's historical behavior.
#
# References:
#  * https://github.com/digital-asset/daml/blob/main/ledger-service/http-json/src/main/scala/com/digitalasset/http/CommandService.scala

from typing import Any, List, Optional, Sequence, Tuple, Union

from ..._gen.com.daml.ledger.api.v1.admin.party_management_service_pb2 import (
    PartyDetails as G_PartyDetails,
)
from ..._gen.com.daml.ledger.api.v1.commands_pb2 import (
    Command as G_Command,
    CreateAndExerciseCommand as G_CreateAndExerciseCommand,
    CreateCommand as G_CreateCommand,
    ExerciseByKeyCommand as G_ExerciseByKeyCommand,
    ExerciseCommand as G_ExerciseCommand,
)
from ..._gen.com.daml.ledger.api.v1.event_pb2 import (
    ArchivedEvent as G_ArchivedEvent,
    CreatedEvent as G_CreatedEvent,
    ExercisedEvent as G_ExercisedEvent,
)
from ..._gen.com.daml.ledger.api.v1.ledger_offset_pb2 import LedgerOffset as G_LedgerOffset
from ..._gen.com.daml.ledger.api.v1.transaction_filter_pb2 import (
    Filters as G_Filters,
    InclusiveFilters as G_InclusiveFilters,
)
from ..._gen.com.daml.ledger.api.v1.transaction_pb2 import TransactionTree as G_TransactionTree
from ..._gen.com.daml.ledger.api.v1.value_pb2 import Identifier as G_Identifier
from ...damlast.daml_lf_1 import (
    DefTemplate,
    DottedName,
    ModuleRef,
    PackageRef,
    TemplateChoice,
    Type,
    TypeConName,
)
from ...damlast.daml_types import con
from ...damlast.protocols import SymbolLookup
from ...damlast.util import module_local_name, module_name, package_ref
from ...prim import ContractData, ContractId
from ...values import Context
from ...values.protobuf import ProtobufDecoder, ProtobufEncoder, set_value
from ..api_types import (
    ArchiveEvent,
    Command,
    CreateAndExerciseCommand,
    CreateCommand,
    CreateEvent,
    ExerciseByKeyCommand,
    ExerciseCommand,
    ExerciseResponse,
    PartyInfo,
)
from ..pkgcache import SHARED_PACKAGE_DATABASE
from ..pkgloader_aio import PackageLoader, PackageService

__all__ = ["Codec"]


class Codec:
    """
    Contains methods for converting to/from Protobuf Ledger API types.

    Some encode/decode methods require package information to be available, which is why a
    connection must be supplied in order to use the codec.

    By default, the package database is _globally_ shared; this is safe to do because we make the
    same assumption that the remote gRPC Ledger API implementation makes: that package IDs uniquely
    identify package contents.
    """

    def __init__(self, conn: PackageService, lookup: Optional[SymbolLookup] = None):
        self.conn = conn
        self._lookup = lookup or SHARED_PACKAGE_DATABASE
        self._loader = PackageLoader(self._lookup, conn)
        self._encode_context = Context(ProtobufEncoder(), self._lookup)
        self._decode_context = Context(ProtobufDecoder(), self._lookup)

    @property
    def lookup(self) -> SymbolLookup:
        return self._lookup

    async def encode_command(self, cmd: Command) -> G_Command:
        if isinstance(cmd, CreateCommand):
            return await self.encode_create_command(cmd.template_id, cmd.payload)
        elif isinstance(cmd, ExerciseCommand):
            return await self.encode_exercise_command(cmd.contract_id, cmd.choice, cmd.argument)
        elif isinstance(cmd, ExerciseByKeyCommand):
            return await self.encode_exercise_by_key_command(
                cmd.template_id, cmd.choice, cmd.key, cmd.argument
            )
        elif isinstance(cmd, CreateAndExerciseCommand):
            return await self.encode_create_and_exercise_command(
                cmd.template_id, cmd.payload, cmd.choice, cmd.argument
            )
        else:
            raise ValueError()

    async def encode_create_command(self, template_id: Any, payload: ContractData) -> G_Command:
        item_type = await self._loader.do_with_retry(
            lambda: self._lookup.template_name(template_id)
        )
        _, value = self._encode_context.convert(con(item_type), payload)
        return G_Command(
            create=G_CreateCommand(
                template_id=self.encode_identifier(item_type), create_arguments=value
            )
        )

    async def encode_exercise_command(
        self,
        contract_id: ContractId,
        choice_name: str,
        argument: Optional[Any] = None,
    ) -> G_ExerciseCommand:
        item_type, _, choice = await self._look_up_choice(contract_id.value_type, choice_name)

        cmd_pb = G_ExerciseCommand(
            template_id=self.encode_identifier(item_type),
            contract_id=contract_id.value,
            choice=choice_name,
        )
        value_field, value_pb = await self.encode_value(choice.arg_binder.type, argument)
        set_value(cmd_pb.choice_argument, value_field, value_pb)

        return G_Command(exercise=cmd_pb)

    async def encode_create_and_exercise_command(
        self,
        template_id: TypeConName,
        payload: ContractData,
        choice_name: str,
        argument: Optional[Any] = None,
    ) -> G_CreateAndExerciseCommand:
        item_type, _, choice = await self._look_up_choice(template_id, choice_name)

        cmd_pb = G_CreateAndExerciseCommand(
            template_id=self.encode_identifier(item_type),
            payload=await self.encode_value(con(item_type), payload),
            choice=choice_name,
        )
        value_field, value_pb = await self.encode_value(choice.arg_binder.type, argument)
        set_value(cmd_pb.choice_argument, value_field, value_pb)

        return G_CreateAndExerciseCommand(createAndExercise=cmd_pb)

    async def encode_exercise_by_key_command(
        self,
        template_id: TypeConName,
        choice_name: str,
        key: Any,
        argument: Optional[ContractData] = None,
    ) -> G_ExerciseByKeyCommand:
        item_type, template, choice = await self._look_up_choice(template_id, choice_name)

        cmd_pb = G_ExerciseByKeyCommand(
            template_id=self.encode_identifier(item_type),
            contract_key=await self.encode_value(template.key.type, key),
            choice=choice_name,
        )
        value_field, value_pb = await self.encode_value(choice.arg_binder.type, argument)
        set_value(cmd_pb.choice_argument, value_field, value_pb)

        return G_Command(exerciseByKey=cmd_pb)

    async def encode_filters(self, template_ids: Sequence[Any]) -> G_Filters:
        # Search for a reference to the "wildcard" template; if any of the requested template_ids
        # is "*", then return results for all templates. We do this first because resolving template
        # IDs otherwise requires do_with_retry, which can be expensive.
        for template_id in template_ids:
            if template_id == "*":
                # if any of the keys references the "wildcard" template, then this means we
                # need to fetch values for all templates; note that we
                return G_Filters()

        # No wildcard template IDs, so inspect and resolve all template references to concrete
        # template IDs
        requested_types = set()
        for template_id in template_ids:
            requested_types.update(
                await self._loader.do_with_retry(lambda: self._lookup.template_names(template_id))
            )

        return G_Filters(
            inclusive=G_InclusiveFilters(
                template_ids=[self.encode_identifier(i) for i in sorted(requested_types)]
            )
        )

    async def encode_value(self, item_type: Type, obj: Any) -> Tuple[str, Optional[Any]]:
        """
        Convert a dazl/Python value to its Protobuf equivalent.
        """
        return await self._loader.do_with_retry(
            lambda: self._encode_context.convert(item_type, obj)
        )

    @staticmethod
    def encode_identifier(name: TypeConName) -> G_Identifier:
        return G_Identifier(
            package_id=package_ref(name),
            module_name=str(module_name(name)),
            entity_name=module_local_name(name),
        )

    @staticmethod
    def encode_begin_offset(offset: Optional[str]) -> G_LedgerOffset:
        return G_LedgerOffset(absolute=offset) if offset is not None else G_LedgerOffset(boundary=0)

    async def decode_created_event(self, event: G_CreatedEvent) -> CreateEvent:
        cid = self.decode_contract_id(event)
        cdata = await self.decode_value(con(cid.value_type), event.create_arguments)
        template = self._lookup.template(cid.value_type)
        key = None
        if template is not None and template.key is not None:
            key = await self.decode_value(template.key.type, event.key)

        return CreateEvent(
            cid, cdata, event.signatories, event.observers, event.agreement_text.value, key
        )

    async def decode_archived_event(self, event: G_ArchivedEvent) -> ArchiveEvent:
        cid = self.decode_contract_id(event)
        return ArchiveEvent(cid)

    async def decode_exercise_response(self, tree: G_TransactionTree) -> ExerciseResponse:
        """
        Convert a Protobuf TransactionTree response to an ExerciseResponse. The TransactionTree is
        expected to only contain a single exercise node at the root level.
        """
        from ... import LOG

        found_choice = None
        result = None
        cid = None

        events = []  # type: List[Union[CreateEvent, ArchiveEvent]]
        for event_id in tree.root_event_ids:
            event_pb = tree.events_by_id[event_id]
            event_pb_type = event_pb.WhichOneof("kind")
            if event_pb_type == "created":
                events.append(await self.decode_created_event(event_pb.created))
            elif event_pb_type == "exercised":
                # Find the "first" exercised node and grab its result value
                if cid is None:
                    cid = self.decode_contract_id(event_pb.exercised)

                    template = self._lookup.template(cid.value_type)

                    if found_choice is None:
                        for choice in template.choices:
                            if choice.name == event_pb.exercised.choice:
                                found_choice = choice
                                break
                        if found_choice is not None:
                            result = await self.decode_value(
                                found_choice.ret_type,
                                event_pb.exercised.exercise_result,
                            )
                        else:
                            LOG.error(
                                "Received an exercise node that referred to a choice that doesn't exist!"
                            )

                events.extend(await self._decode_exercised_child_events(tree, [event_id]))
            else:
                LOG.warning("Received an unknown event type: %s", event_pb_type)

        return ExerciseResponse(result, events)

    async def _decode_exercised_child_events(
        self, tree: G_TransactionTree, event_ids: Sequence[str]
    ) -> Sequence[Union[CreateEvent, ArchiveEvent]]:
        from ... import LOG

        events = []  # type: List[Union[CreateEvent, ArchiveEvent]]
        for event_id in event_ids:
            event_pb = tree.events_by_id[event_id]
            event_pb_type = event_pb.WhichOneof("kind")
            if event_pb_type == "created":
                events.append(await self.decode_created_event(event_pb.created))
            elif event_pb_type == "exercised":
                if event_pb.exercised.consuming:
                    events.append(ArchiveEvent(self.decode_contract_id(event_pb.exercised)))
                events.extend(
                    await self._decode_exercised_child_events(
                        tree, event_pb.exercised.child_event_ids
                    )
                )
            else:
                LOG.warning("Received an unknown event type: %s", event_pb_type)
        return events

    async def decode_value(self, item_type: Type, obj: Any) -> Optional[Any]:
        """
        Convert a Protobuf Ledger API value to its dazl/Python equivalent.
        """
        return await self._loader.do_with_retry(
            lambda: self._decode_context.convert(item_type, obj)
        )

    @staticmethod
    def decode_contract_id(
        event: Union[G_CreatedEvent, G_ExercisedEvent, G_ArchivedEvent],
    ) -> ContractId:
        vt = Codec.decode_identifier(event.template_id)
        return ContractId(vt, event.contract_id)

    @staticmethod
    def decode_identifier(identifier: G_Identifier) -> TypeConName:
        return TypeConName(
            ModuleRef(
                PackageRef(identifier.package_id), DottedName(identifier.module_name.split("."))
            ),
            DottedName(identifier.entity_name.split(".")).segments,
        )

    @staticmethod
    def decode_party_info(party_details: G_PartyDetails) -> PartyInfo:
        return PartyInfo(party_details.party, party_details.display_name, party_details.is_local)

    async def _look_up_choice(
        self, template_id: Any, choice_name: str
    ) -> Tuple[TypeConName, DefTemplate, TemplateChoice]:
        template_type = await self._loader.do_with_retry(
            lambda: self._lookup.template_name(template_id)
        )
        template = self._lookup.template(template_type)
        for choice in template.choices:
            if choice.name == choice_name:
                return template_type, template, choice
        raise ValueError(f"template {template.tycon} has no choice named {choice_name}")
