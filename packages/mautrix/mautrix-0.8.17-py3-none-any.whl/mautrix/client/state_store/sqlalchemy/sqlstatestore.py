# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Dict, Optional, List

from mautrix.types import (UserID, RoomID, Membership, Member, PowerLevelStateEventContent,
                           RoomEncryptionStateEventContent)

from ..abstract import StateStore
from .mx_user_profile import UserProfile
from .mx_room_state import RoomState


class SQLStateStore(StateStore):
    _profile_cache: Dict[RoomID, Dict[UserID, UserProfile]]
    _room_state_cache: Dict[RoomID, RoomState]

    def __init__(self) -> None:
        super().__init__()
        self._profile_cache = {}
        self._room_state_cache = {}

    def _get_user_profile(self, room_id: RoomID, user_id: UserID, create: bool = False
                          ) -> UserProfile:
        if not room_id:
            raise ValueError("room_id is empty")
        elif not user_id:
            raise ValueError("user_id is empty")
        try:
            return self._profile_cache[room_id][user_id]
        except KeyError:
            pass
        if room_id not in self._profile_cache:
            self._profile_cache[room_id] = {}

        profile = UserProfile.get(room_id, user_id)
        if profile:
            self._profile_cache[room_id][user_id] = profile
        elif create:
            profile = UserProfile(room_id=room_id, user_id=user_id, membership=Membership.LEAVE)
            profile.insert()
            self._profile_cache[room_id][user_id] = profile
        return profile

    async def get_member(self, room_id: RoomID, user_id: UserID) -> Optional[Member]:
        profile = self._get_user_profile(room_id, user_id)
        if not profile:
            return None
        return profile.member()

    async def set_member(self, room_id: RoomID, user_id: UserID, member: Member) -> None:
        if not member:
            raise ValueError("member info is empty")
        profile = self._get_user_profile(room_id, user_id, create=True)
        profile.edit(membership=member.membership,
                     displayname=member.displayname or profile.displayname,
                     avatar_url=member.avatar_url or profile.avatar_url)

    async def set_membership(self, room_id: RoomID, user_id: UserID,
                             membership: Membership) -> None:
        await self.set_member(room_id, user_id, Member(membership=membership))

    async def get_members(self, room_id: RoomID) -> Optional[List[UserID]]:
        self._profile_cache[room_id] = {}
        for profile in UserProfile.all_in_room(room_id):
            self._profile_cache[room_id][profile.user_id] = profile
        return [profile.user_id for profile in self._profile_cache[room_id].values()]

    async def get_members_filtered(self, room_id: RoomID, not_prefix: str, not_suffix: str,
                                   not_id: str) -> Optional[List[UserID]]:
        return [profile.user_id for profile
                in UserProfile.all_in_room(room_id, not_suffix, not_prefix, not_id)]

    async def set_members(self, room_id: RoomID, members: Dict[UserID, Member]) -> None:
        UserProfile.bulk_replace(room_id, members)
        self._get_room_state(room_id, create=True).edit(has_full_member_list=True)
        try:
            del self._profile_cache[room_id]
        except KeyError:
            pass

    async def has_full_member_list(self, room_id: RoomID) -> bool:
        room = self._get_room_state(room_id)
        if not room:
            return False
        return room.has_full_member_list

    async def find_shared_rooms(self, user_id: UserID) -> List[RoomID]:
        return [profile.room_id for profile in UserProfile.find_rooms_with_user(user_id)]

    def _get_room_state(self, room_id: RoomID, create: bool = False) -> RoomState:
        if not room_id:
            raise ValueError("room_id is empty")
        try:
            return self._room_state_cache[room_id]
        except KeyError:
            pass

        room = RoomState.get(room_id)
        if room:
            self._room_state_cache[room_id] = room
        elif create:
            room = RoomState(room_id=room_id)
            room.insert()
            self._room_state_cache[room_id] = room
        return room

    async def has_power_levels_cached(self, room_id: RoomID) -> bool:
        room = self._get_room_state(room_id)
        if not room:
            return False
        return room.has_power_levels

    async def get_power_levels(self, room_id: RoomID) -> Optional[PowerLevelStateEventContent]:
        room = self._get_room_state(room_id)
        if not room:
            return None
        return room.power_levels

    async def set_power_levels(self, room_id: RoomID, content: PowerLevelStateEventContent) -> None:
        if not content:
            raise ValueError("content is empty")
        self._get_room_state(room_id, create=True).edit(power_levels=content)

    async def is_encrypted(self, room_id: RoomID) -> Optional[bool]:
        room = self._get_room_state(room_id)
        if not room:
            return None
        return room.is_encrypted

    async def has_encryption_info_cached(self, room_id: RoomID) -> bool:
        room = self._get_room_state(room_id)
        return room and room.has_encryption_info

    async def get_encryption_info(self, room_id: RoomID) -> Optional[RoomEncryptionStateEventContent]:
        room = self._get_room_state(room_id)
        if not room:
            return None
        return room.encryption

    async def set_encryption_info(self, room_id: RoomID,
                                  content: RoomEncryptionStateEventContent) -> None:
        if not content:
            raise ValueError("content is empty")
        self._get_room_state(room_id, create=True).edit(encryption=content, is_encrypted=True)
