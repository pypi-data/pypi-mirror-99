# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import cast, Optional, List, Set, Tuple
from datetime import datetime, timedelta

import olm

from mautrix.types import (UserID, DeviceID, IdentityKey, SigningKey, RoomID, OlmMsgType,
                           RoomKeyEventContent, EncryptionAlgorithm, OlmCiphertext)
from mautrix.errors import EncryptionError


class Session(olm.Session):
    creation_time: datetime
    use_time: datetime

    def __init__(self):
        super().__init__()
        self.creation_time = datetime.now()
        self.use_time = datetime.now()

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @property
    def expired(self):
        return False

    @classmethod
    def from_pickle(cls, pickle: bytes, passphrase: str, creation_time: datetime,
                    use_time: Optional[datetime] = None) -> 'Session':
        session = super().from_pickle(pickle, passphrase=passphrase)
        session.creation_time = creation_time
        session.use_time = use_time or creation_time
        return session

    def matches(self, ciphertext: str) -> bool:
        return super().matches(olm.OlmPreKeyMessage(ciphertext))

    def decrypt(self, ciphertext: OlmCiphertext) -> str:
        self.use_time = datetime.now()
        return super().decrypt(olm.OlmPreKeyMessage(ciphertext.body)
                               if ciphertext.type == OlmMsgType.PREKEY
                               else olm.OlmMessage(ciphertext.body))

    def encrypt(self, plaintext: str) -> OlmCiphertext:
        self.use_time = datetime.now()
        result = super().encrypt(plaintext)
        return OlmCiphertext(type=(OlmMsgType.PREKEY if isinstance(result, olm.OlmPreKeyMessage)
                                   else OlmMsgType.MESSAGE),
                             body=result.ciphertext)


class InboundGroupSession(olm.InboundGroupSession):
    room_id: RoomID
    signing_key: SigningKey
    sender_key: IdentityKey
    forwarding_chain: List[str]

    def __init__(self, session_key: str, signing_key: SigningKey, sender_key: IdentityKey,
                 room_id: RoomID, forwarding_chain: Optional[List[str]] = None) -> None:
        self.signing_key = signing_key
        self.sender_key = sender_key
        self.room_id = room_id
        self.forwarding_chain = forwarding_chain or []
        super().__init__(session_key)

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @classmethod
    def from_pickle(cls, pickle: bytes, passphrase: str, signing_key: SigningKey,
                    sender_key: IdentityKey, room_id: RoomID,
                    forwarding_chain: Optional[List[str]] = None) -> 'InboundGroupSession':
        session = super().from_pickle(pickle, passphrase)
        session.signing_key = signing_key
        session.sender_key = sender_key
        session.room_id = room_id
        session.forwarding_chain = forwarding_chain or []
        return session

    @classmethod
    def import_session(cls, session_key: str, signing_key: SigningKey, sender_key: IdentityKey,
                       room_id: RoomID, forwarding_chain: Optional[List[str]] = None
                       ) -> 'InboundGroupSession':
        session = super().import_session(session_key)
        session.signing_key = signing_key
        session.sender_key = sender_key
        session.room_id = room_id
        session.forwarding_chain = forwarding_chain or []
        return session


class OutboundGroupSession(olm.OutboundGroupSession):
    """Outbound group session aware of the users it is shared with.

    Also remembers the time it was created and the number of messages it has
    encrypted, in order to know if it needs to be rotated.
    """

    max_age: timedelta
    max_messages: int
    creation_time: datetime
    use_time: datetime
    message_count: int

    room_id: RoomID
    users_shared_with: Set[Tuple[UserID, DeviceID]]
    users_ignored: Set[Tuple[UserID, DeviceID]]
    shared: bool

    def __init__(self, room_id: RoomID) -> None:
        self.max_age = timedelta(days=7)
        self.max_messages = 100
        self.creation_time = datetime.now()
        self.use_time = datetime.now()
        self.message_count = 0
        self.room_id = room_id
        self.users_shared_with = set()
        self.users_ignored = set()
        self.shared = False
        super().__init__()

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @property
    def expired(self):
        return (self.message_count >= self.max_messages
                or datetime.now() - self.creation_time >= self.max_age)

    def encrypt(self, plaintext):
        if not self.shared:
            raise EncryptionError("Group session has not been shared")

        if self.expired:
            raise EncryptionError("Group session has expired")

        self.message_count += 1
        self.use_time = datetime.now()
        return super().encrypt(plaintext)

    @classmethod
    def from_pickle(cls, pickle: bytes, passphrase: str, max_age: timedelta, max_messages: int,
                    creation_time: datetime, use_time: datetime, message_count: int,
                    room_id: RoomID, shared: bool) -> 'OutboundGroupSession':
        session = cast(OutboundGroupSession, super().from_pickle(pickle, passphrase))
        session.max_age = max_age
        session.max_messages = max_messages
        session.creation_time = creation_time
        session.use_time = use_time
        session.message_count = message_count
        session.room_id = room_id
        session.users_shared_with = set()
        session.users_ignored = set()
        session.shared = shared
        return session

    @property
    def share_content(self) -> RoomKeyEventContent:
        return RoomKeyEventContent(algorithm=EncryptionAlgorithm.MEGOLM_V1, room_id=self.room_id,
                                   session_id=self.id, session_key=self.session_key)
