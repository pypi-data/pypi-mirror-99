from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleApplicationPropertyBean")


@attr.s(auto_attribs=True)
class SimpleApplicationPropertyBean:
    """  """

    id: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        value = d.pop("value", UNSET)

        simple_application_property_bean = cls(
            id=id,
            value=value,
        )

        return simple_application_property_bean
