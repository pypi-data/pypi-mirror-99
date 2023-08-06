import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.field_last_used_type import FieldLastUsedType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldLastUsed")


@attr.s(auto_attribs=True)
class FieldLastUsed:
    """ Information about the most recent use of a field. """

    type: Union[Unset, FieldLastUsedType] = UNSET
    value: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, FieldLastUsedType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        value: Union[Unset, str] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type: Union[Unset, FieldLastUsedType] = UNSET
        _type = d.pop("type", UNSET)
        if not isinstance(_type, Unset):
            type = FieldLastUsedType(_type)

        value: Union[Unset, datetime.datetime] = UNSET
        _value = d.pop("value", UNSET)
        if not isinstance(_value, Unset):
            value = isoparse(_value)

        field_last_used = cls(
            type=type,
            value=value,
        )

        return field_last_used
