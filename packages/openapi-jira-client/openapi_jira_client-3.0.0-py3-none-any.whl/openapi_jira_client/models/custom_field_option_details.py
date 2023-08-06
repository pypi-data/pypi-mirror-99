from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldOptionDetails")


@attr.s(auto_attribs=True)
class CustomFieldOptionDetails:
    """ Details of a custom field option and its cascading options. """

    id: Union[Unset, int] = UNSET
    value: Union[Unset, str] = UNSET
    cascading_options: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        value = self.value
        cascading_options: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.cascading_options, Unset):
            cascading_options = self.cascading_options

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if value is not UNSET:
            field_dict["value"] = value
        if cascading_options is not UNSET:
            field_dict["cascadingOptions"] = cascading_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        value = d.pop("value", UNSET)

        cascading_options = cast(List[str], d.pop("cascadingOptions", UNSET))

        custom_field_option_details = cls(
            id=id,
            value=value,
            cascading_options=cascading_options,
        )

        return custom_field_option_details
