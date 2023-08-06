from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionHolder")


@attr.s(auto_attribs=True)
class PermissionHolder:
    """ Details of a user, group, field, or project role that holds a permission. See [Holder object](#holder-object) in *Get all permission schemes* for more information. """

    type: str
    parameter: Union[Unset, str] = UNSET
    expand: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        parameter = self.parameter
        expand = self.expand

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
            }
        )
        if parameter is not UNSET:
            field_dict["parameter"] = parameter
        if expand is not UNSET:
            field_dict["expand"] = expand

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        parameter = d.pop("parameter", UNSET)

        expand = d.pop("expand", UNSET)

        permission_holder = cls(
            type=type,
            parameter=parameter,
            expand=expand,
        )

        return permission_holder
