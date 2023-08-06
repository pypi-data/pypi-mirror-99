# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Optional, Type
import json

from sqlalchemy import Column, Text, Boolean, types

from mautrix.types import (RoomID, PowerLevelStateEventContent as PowerLevels,
                           RoomEncryptionStateEventContent as EncryptionInfo, Serializable)
from mautrix.util.db import Base


class SerializableType(types.TypeDecorator):
    impl = types.Text

    def __init__(self, python_type: Type[Serializable], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._python_type = python_type

    @property
    def python_type(self) -> Type[Serializable]:
        return self._python_type

    def process_bind_param(self, value: Serializable, dialect) -> Optional[str]:
        if value is not None:
            return json.dumps(value.serialize())
        return None

    def process_result_value(self, value: str, dialect) -> Optional[Serializable]:
        if value is not None:
            return self.python_type.deserialize(json.loads(value))
        return None

    def process_literal_param(self, value, dialect):
        return value


class RoomState(Base):
    __tablename__ = "mx_room_state"

    room_id: RoomID = Column(Text, primary_key=True)
    is_encrypted: bool = Column(Boolean, nullable=True)
    has_full_member_list: bool = Column(Boolean, nullable=True)
    encryption: EncryptionInfo = Column(SerializableType(EncryptionInfo), nullable=True)
    power_levels: PowerLevels = Column(SerializableType(PowerLevels), nullable=True)

    @property
    def has_power_levels(self) -> bool:
        return bool(self.power_levels)

    @property
    def has_encryption_info(self) -> bool:
        return self.is_encrypted is not None

    @classmethod
    def get(cls, room_id: RoomID) -> Optional['RoomState']:
        return cls._select_one_or_none(cls.c.room_id == room_id)
