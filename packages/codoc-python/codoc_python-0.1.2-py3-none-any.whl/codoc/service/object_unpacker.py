#!/usr/bin/env python3
import inspect
from typing import Set, Tuple

from codoc.domain.model import Node

from .parsing.types import ObjectType
from .parsing.utils import is_not_an_instance

NodeTuple = Tuple[ObjectType, Node]


def recursively_get_all_subobjects_in_object(obj: ObjectType):
    return RecursiveObjectFetcher(obj).get_all_objects_in_object_and_sub_objects()


class RecursiveObjectFetcher:
    def __init__(self, obj: ObjectType):
        self._obj = obj
        self._module_name = get_name_of_module(self._obj)

    def get_all_objects_in_object_and_sub_objects(self) -> Set[ObjectType]:
        return self.get_all_objects_in_sub_objects() | self.get_all_objects()

    def get_all_objects(
        self,
    ) -> Set[ObjectType]:

        return set(
            self.denote_parent(obj)
            for name, obj in inspect.getmembers(self._obj)
            if self._is_obj_valid_for_return(name, obj)
        ) | {self._obj}

    def denote_parent(self, obj: ObjectType) -> ObjectType:
        if inspect.isclass(self._obj):
            obj.__parentclass__ = self._obj
        return obj

    def get_all_objects_in_sub_objects(self) -> Set[ObjectType]:
        return set(
            inner_obj
            for obj in self.get_all_objects()
            if self._is_obj_part_of_module(obj) and obj is not self._obj
            for inner_obj in RecursiveObjectFetcher(
                obj
            ).get_all_objects_in_object_and_sub_objects()
        )

    def _is_obj_part_of_module(self, obj: ObjectType) -> bool:
        module_name = get_name_of_module(obj)
        return module_name is not None and module_name.startswith(self._module_name)

    def _is_obj_valid_for_return(self, name: str, obj: object) -> bool:
        return (
            not name.startswith("__")
            and is_not_an_instance(obj)
            and self._is_obj_part_of_module(obj)
        )


def get_name_of_module(obj: object) -> str:
    return obj.__name__ if inspect.ismodule(obj) else getattr(obj, "__module__", None)
