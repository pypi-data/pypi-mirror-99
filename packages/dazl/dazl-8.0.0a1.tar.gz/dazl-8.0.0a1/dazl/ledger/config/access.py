# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import base64
from collections.abc import MutableSet as MutableSetBase, Set as SetBase
import json
from logging import Logger
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Collection,
    Iterator,
    Mapping,
    MutableSet,
    Optional,
    Protocol,
    Union,
    runtime_checkable,
)

from ...prim import Party
from .exc import ConfigError

__all__ = [
    "AccessConfig",
    "TokenBasedAccessConfig",
    "PropertyBasedAccessConfig",
    "PartyRights",
    "PartyRightsSet",
    "create_access",
]

if TYPE_CHECKING:
    # We refer to the Config class in a docstring and
    # without this import, Sphinx can't resolve the reference
    # noinspection PyUnresolvedReferences
    from . import Config


def parties_from_env(*env_vars: str) -> AbstractSet[Party]:
    """
    Read the set of parties
    """
    return {Party(p) for env_var in env_vars for p in os.getenv(env_var, "").split(",") if p}


# mypy note: typing.overload cannot properly express a more correct signature for this function,
#  which is that if oauth_token is supplied, then a TokenBasedAccessConfig class is returned and
#  otherwise, a PropertyBasedAccessConfig class is returned. Trying to type this properly with
#  overloads results in:
#     "Not all union combinations were tried because there are too many unions"
#  It's also worth nothing that our only usage of this function also supplies all parameters since
#  we're effectively just passing **kwargs around, so it's not clear a more accurate type helps much
#  anyway.
def create_access(
    *,
    read_as: Union[None, Party, Collection[Party]] = None,
    act_as: Union[None, Party, Collection[Party]] = None,
    admin: Optional[bool] = None,
    ledger_id: Optional[str] = None,
    application_name: Optional[str] = None,
    oauth_token: Optional[str] = None,
    oauth_token_file: Optional[str] = None,
    logger: Optional[Logger] = None,
) -> AccessConfig:
    """
    Create an appropriate instance of :class:`AccessConfig`.

    See :meth:`Config.create` for a more detailed description of these parameters.
    """
    # admin = None is effectively the same as admin = False in this context
    is_property_based = read_as or act_as or admin or ledger_id or application_name
    if not is_property_based and not oauth_token and not oauth_token_file:
        # none of the access-related parameters were passed in, so try to read some from the
        # environment
        act_as = parties_from_env("DAML_LEDGER_ACT_AS", "DAML_LEDGER_PARTY")
        read_as = parties_from_env("DAML_LEDGER_READ_AS", "DABL_PUBLIC_PARTY")
        ledger_id = os.getenv("DAML_LEDGER_ID", "")
        application_name = os.getenv("DAML_LEDGER_APPLICATION_NAME")
        oauth_token = os.getenv("DAML_LEDGER_OAUTH_TOKEN")
        oauth_token_file = os.getenv("DAML_LEDGER_OAUTH_TOKEN_FILE")

    is_property_based = read_as or act_as or admin or ledger_id or application_name
    if not is_property_based and not oauth_token and not oauth_token_file:
        raise ConfigError("no oauth token access or read_as/act_as/admin was specified")

    # how do they configure thee? let me count the ways...
    if sum(map(int, (bool(is_property_based), bool(oauth_token), bool(oauth_token_file)))) > 1:
        raise ConfigError(
            "must specify ONE of read_as/act_as/admin, oauth_token, or oauth_token_file"
        )

    if oauth_token_file:
        return TokenFileBasedAccessConfig(oauth_token_file)
    elif oauth_token:
        return TokenBasedAccessConfig(oauth_token)
    else:
        return PropertyBasedAccessConfig(
            read_as=read_as,
            act_as=act_as,
            admin=admin,
            ledger_id=ledger_id,
            application_name=application_name,
        )


@runtime_checkable
class AccessConfig(Protocol):
    """
    Configuration parameters for providing access to a ledger.

    To create an instance of this protocol, call :func:`create_access` and provide *either*
    ``oauth_token`` *or* the other fields you wish to set (such as ``act_as``). You cannot specify
    both an access token and other fields.

    You may implement this protocol using your own custom type if you have very specialized access
    needs.
    """

    @property
    def read_as(self) -> AbstractSet[Party]:
        """
        The set of parties that can be used to read data from the ledger. This also includes the
        set of parties that can be used to write data to the ledger.

        :type: AbstractSet[Party]
        """
        raise NotImplementedError

    @property
    def read_only_as(self) -> AbstractSet[Party]:
        """
        The set of parties that have read-only access to the underlying ledger.

        :type: AbstractSet[Party]
        """
        raise NotImplementedError

    @property
    def act_as(self) -> AbstractSet[Party]:
        """
        The set of parties that can be used to write data to the ledger.

        :type: AbstractSet[Party]
        """
        raise NotImplementedError

    @property
    def admin(self) -> bool:
        """
        ``True`` if the token grants "admin" access.

        :type: bool
        """
        raise NotImplementedError

    @property
    def ledger_id(self) -> Optional[str]:
        """
        The ledger ID. For non-token based access methods, this can be queried from the ledger.

        :type: Optional[str]
        """
        raise NotImplementedError

    @property
    def application_name(self) -> str:
        """
        The application name.

        :type: str
        """
        raise NotImplementedError

    @property
    def token(self) -> str:
        """
        The bearer token that provides authorization and authentication to a ledger.

        :type: str
        """
        raise NotImplementedError


class TokenBasedAccessConfig(AccessConfig):
    """
    Access configuration that is inherently token-based. The token can be changed at any time, and
    party rights, the application name, and ledger ID are all derived off of the token.
    """

    def __init__(self, oauth_token: str):
        """
        Initialize a token-based access configuration.

        :param oauth_token: The initial value of the bearer token.
        """
        self.token = oauth_token

    @property
    def token(self) -> str:
        """
        The bearer token that provides authorization and authentication to a ledger. This value can
        be replaced on a live connection in order to support use cases such as token refreshing.
        """
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        self._token = value
        claims = decode_token(self._token)

        read_as = frozenset(claims.get("readAs", ()))
        act_as = frozenset(claims.get("actAs", ()))

        self._act_as = act_as
        self._read_only_as = read_as - act_as
        self._read_as = read_as.union(act_as)
        self._admin = bool(claims.get("admin", False))
        self._ledger_id = claims.get("ledgerId", None)
        self._application_name = claims.get("applicationId", None)

    @property
    def read_as(self) -> AbstractSet[Party]:
        return self._read_as

    @property
    def read_only_as(self) -> AbstractSet[Party]:
        return self._read_only_as

    @property
    def act_as(self) -> AbstractSet[Party]:
        return self._act_as

    @property
    def admin(self) -> bool:
        return self._admin

    @property
    def ledger_id(self) -> Optional[str]:
        return self._ledger_id

    @property
    def application_name(self) -> str:
        return self._application_name


class TokenFileBasedAccessConfig(TokenBasedAccessConfig):
    def __init__(self, oauth_token_file: str):
        # TODO: Update the token when the contents of this file change.
        super().__init__(Path(oauth_token_file).read_text())


class PropertyBasedAccessConfig(AccessConfig):
    """
    Access configuration that is manually specified outside of an authentication/authorization
    framework. Suitable for local testing or when no auth server is available, and the Ledger API
    inherently trusts any caller to provide its own authentication and authorization.
    """

    def __init__(
        self,
        read_as: Union[None, Party, Collection[Party]] = None,
        act_as: Union[None, Party, Collection[Party]] = None,
        admin: Optional[bool] = False,
        ledger_id: Optional[str] = None,
        application_name: Optional[str] = None,
    ):
        """
        Initialize a property-based access configuration.

        :param read_as:
            A party or set of parties on whose behalf (in addition to all parties listed in ``act_as``)
            contracts can be retrieved.
        :param act_as:
            A party or set of parties on whose behalf commands should be executed. Parties here are also
            implicitly granted ``read_as`` access as well.
        :param admin:
            HTTP JSON API only: allow admin endpoints to be used. This flag is ignored when connecting
            to gRPC Ledger API implementations.
        :param ledger_id:
            The ledger ID to connect to. For the HTTP JSON API, this value is required. For the gRPC
            Ledger API, if this value is _not_ supplied, its value will be retrieved from the server.
        :param application_name:
            A string that identifies this application. This is used for tracing purposes on the
            server-side.
        """
        self._parties = PartyRights()
        self._parties.maybe_add(read_as, False)
        self._parties.maybe_add(act_as, True)
        self._admin = bool(admin)
        self._ledger_id = ledger_id
        self._application_name = application_name or "dazl-client"

    @property
    def token(self):
        """
        Produces a token without signing, utilizing our parameters.
        """
        return encode_unsigned_token(
            self.read_as, self.act_as, self.ledger_id, self.application_name, self.admin
        )

    @property
    def ledger_id(self) -> "Optional[str]":
        """
        The ledger ID. When connecting to the gRPC Ledger API, this can be inferred and does not
        need to be supplied. When connecting to the HTTP JSON API, it must be supplied.

        :type: Optional[str]
        """
        return self._ledger_id

    @ledger_id.setter
    def ledger_id(self, value: "Optional[str]") -> None:
        self._ledger_id = value

    @property
    def application_name(self) -> str:
        return self._application_name

    @property
    def read_as(self) -> "AbstractSet[Party]":
        """
        The set of parties for which read rights are granted. This collection is read-only. If you
        want to add a party with read-only access, add it to :meth:`read_only_as`; if you want to
        add a party with act-as access as well as read-only access, add it to :meth:`act_as`.

        This set always includes the act_as parties. For the set of parties that can be read as
        but NOT acted as, use :meth:`read_only_as`.

        :type: AbstractSet[Party]
        """
        return self._parties

    @property
    def read_only_as(self) -> "MutableSet[Party]":
        """
        The set of parties for which read-as rights are granted, but act-as rights are NOT granted.
        This collection can be modified.

        :type: MutableSet[Party]
        """
        return self._parties.read_as

    @property
    def act_as(self) -> "MutableSet[Party]":
        """
        The set of parties for which act-as rights are granted. This collection can be modified.
        Adding a party to this set _removes_ it from :meth:`read_only_as`.

        :type: MutableSet[Party]
        """
        return self._parties.act_as

    @property
    def admin(self) -> bool:
        """
        Whether or not the token sent to HTTP JSON API contains the ``admin: true`` flag that
        signals a token bearer with admin access.
        """
        return self._admin

    @admin.setter
    def admin(self, value: bool) -> None:
        self._admin = value


def parties(p: Union[None, Party, Collection[Party]]) -> Collection[Party]:
    if p is None:
        return []
    elif isinstance(p, str):
        return [Party(p)]
    else:
        return p


DamlLedgerApiNamespace = "https://daml.com/ledger-api"


def decode_token(token: str) -> Mapping[str, Any]:
    components = token.split(".", 3)
    if len(components) != 3:
        raise ValueError("not a JWT")
    claim_str = base64.urlsafe_b64decode(components[1])
    claims = json.loads(claim_str)
    claims_dict = claims.get(DamlLedgerApiNamespace)
    if claims_dict is None:
        raise ValueError(f"JWT is missing claim namespace: {DamlLedgerApiNamespace!r}")
    return claims_dict


def encode_unsigned_token(
    read_as: Collection[Party],
    act_as: Collection[Party],
    ledger_id: str,
    application_id: str,
    admin: bool = True,
) -> bytes:
    header = {
        "alg": "none",
        "typ": "JWT",
    }
    payload = {
        DamlLedgerApiNamespace: {
            "ledgerId": ledger_id,
            "applicationId": application_id,
            "actAs": sorted(act_as),
            "readAs": sorted(read_as),
            "admin": admin,
        }
    }

    return (
        base64.urlsafe_b64encode(json.dumps(header).encode("utf-8"))
        + b"."
        + base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8"))
        + b"."
    )


class PartyRights(SetBase):
    __slots__ = ("_rights", "read_as", "act_as")

    def __init__(self):
        self._rights = dict()
        self.read_as = PartyRightsSet(self, False)
        self.act_as = PartyRightsSet(self, True)

    def maybe_add(
        self, value: "Union[None, Party, Collection[Party]]", has_act_rights: bool
    ) -> None:
        if value is None:
            return

        # Party is a fake Python newtype, so isinstance checks don't work on it
        if isinstance(value, str):
            self.add(Party(value), has_act_rights)
        else:
            for party in value:
                self.add(party, has_act_rights)

    def add(self, value: "Party", has_act_rights: bool) -> None:
        """
        Add/replace a ``Party`` and its rights.
        """
        self._rights[value] = has_act_rights

    def discard(self, value: "Party") -> None:
        self._rights.pop(value)

    def get(self, value: "Party") -> "Optional[bool]":
        return self._rights.get(value)

    def count(self, act_as: bool) -> int:
        return sum(1 for p, a in self._rights.items() if act_as == a)

    def __contains__(self, party: object) -> bool:
        return party in self._rights

    def __len__(self) -> int:
        return len(self._rights)

    def __iter__(self) -> "Iterator[Party]":
        return iter(sorted(self._rights))

    def iter(self, act_as: bool) -> "Iterator[Party]":
        return iter(p for p, a in sorted(self._rights.items()) if a == act_as)


class PartyRightsSet(MutableSetBase):
    def __init__(self, rights: "PartyRights", act_as: bool):
        self._rights = rights
        self._act_as = act_as

    def add(self, value: "Party") -> None:
        self._rights.add(value, self._act_as)

    def discard(self, value: "Party") -> None:
        self._rights.discard(value)

    def __contains__(self, obj: "object") -> bool:
        return isinstance(obj, str) and (self._rights.get(Party(obj)) == self._act_as)

    def __len__(self) -> int:
        return self._rights.count(self._act_as)

    def __iter__(self) -> "Iterator[Party]":
        return self._rights.iter(self._act_as)
