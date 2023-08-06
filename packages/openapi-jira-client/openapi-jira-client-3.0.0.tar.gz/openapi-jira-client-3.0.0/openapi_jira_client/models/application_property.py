from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationProperty")


@attr.s(auto_attribs=True)
class ApplicationProperty:
    """ Details of an application property. """

    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    desc: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    default_value: Union[Unset, str] = UNSET
    example: Union[Unset, str] = UNSET
    allowed_values: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        key = self.key
        value = self.value
        name = self.name
        desc = self.desc
        type = self.type
        default_value = self.default_value
        example = self.example
        allowed_values: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.allowed_values, Unset):
            allowed_values = self.allowed_values

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value
        if name is not UNSET:
            field_dict["name"] = name
        if desc is not UNSET:
            field_dict["desc"] = desc
        if type is not UNSET:
            field_dict["type"] = type
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value
        if example is not UNSET:
            field_dict["example"] = example
        if allowed_values is not UNSET:
            field_dict["allowedValues"] = allowed_values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        value = d.pop("value", UNSET)

        name = d.pop("name", UNSET)

        desc = d.pop("desc", UNSET)

        type = d.pop("type", UNSET)

        default_value = d.pop("defaultValue", UNSET)

        example = d.pop("example", UNSET)

        allowed_values = cast(List[str], d.pop("allowedValues", UNSET))

        application_property = cls(
            id=id,
            key=key,
            value=value,
            name=name,
            desc=desc,
            type=type,
            default_value=default_value,
            example=example,
            allowed_values=allowed_values,
        )

        return application_property
