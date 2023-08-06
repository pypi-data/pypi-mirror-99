from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.visibility_type import VisibilityType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Visibility")


@attr.s(auto_attribs=True)
class Visibility:
    """ The group or role to which this item is visible. """

    type: Union[Unset, VisibilityType] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, VisibilityType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type: Union[Unset, VisibilityType] = UNSET
        _type = d.pop("type", UNSET)
        if not isinstance(_type, Unset):
            type = VisibilityType(_type)

        value = d.pop("value", UNSET)

        visibility = cls(
            type=type,
            value=value,
        )

        visibility.additional_properties = d
        return visibility

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
