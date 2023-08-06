# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Optional
from abc import ABC, abstractmethod

from ruamel.yaml.comments import CommentedMap

from .recursive_dict import RecursiveDict


class BaseMissingError(ValueError):
    pass


class ConfigUpdateHelper:
    base: RecursiveDict[CommentedMap]

    def __init__(self, base: RecursiveDict, config: RecursiveDict) -> None:
        self.base = base
        self.source = config

    def copy(self, from_path: str, to_path: Optional[str] = None) -> None:
        if from_path in self.source:
            self.base[to_path or from_path] = self.source[from_path]

    def copy_dict(self, from_path: str, to_path: Optional[str] = None,
                  override_existing_map: Optional[bool] = True) -> None:
        if from_path in self.source:
            to_path = to_path or from_path
            if override_existing_map or to_path not in self.base:
                self.base[to_path] = CommentedMap()
            for key, value in self.source[from_path].items():
                self.base[to_path][key] = value

    def __iter__(self):
        yield self.copy
        yield self.copy_dict
        yield self.base


class BaseConfig(ABC, RecursiveDict[CommentedMap]):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def load_base(self) -> Optional[RecursiveDict[CommentedMap]]:
        pass

    def load_and_update(self) -> None:
        self.load()
        self.update()

    @abstractmethod
    def save(self) -> None:
        pass

    def update(self, save: bool = True) -> None:
        base = self.load_base()
        if not base:
            raise BaseMissingError("Can't update() without base config")

        self.do_update(ConfigUpdateHelper(base, self))
        self._data = base._data
        if save:
            self.save()

    @abstractmethod
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        pass
