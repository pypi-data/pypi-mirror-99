from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.user_permission import UserPermission
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionsPermissions")


@attr.s(auto_attribs=True)
class PermissionsPermissions:
    """ List of permissions. """

    additional_properties: Dict[str, UserPermission] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions_permissions = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = UserPermission.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        permissions_permissions.additional_properties = additional_properties
        return permissions_permissions

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> UserPermission:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: UserPermission) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
