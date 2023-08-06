from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldUpdateOperation")


@attr.s(auto_attribs=True)
class FieldUpdateOperation:
    """ Details of an operation to perform on a field. """

    add: Union[Unset, None] = UNSET
    set: Union[Unset, None] = UNSET
    remove: Union[Unset, None] = UNSET
    edit: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        add = None

        set = None

        remove = None

        edit = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if add is not UNSET:
            field_dict["add"] = add
        if set is not UNSET:
            field_dict["set"] = set
        if remove is not UNSET:
            field_dict["remove"] = remove
        if edit is not UNSET:
            field_dict["edit"] = edit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        add = None

        set = None

        remove = None

        edit = None

        field_update_operation = cls(
            add=add,
            set=set,
            remove=remove,
            edit=edit,
        )

        return field_update_operation
