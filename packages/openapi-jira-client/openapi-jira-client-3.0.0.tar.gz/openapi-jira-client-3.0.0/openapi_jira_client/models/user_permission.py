from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user_permission_type import UserPermissionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPermission")


@attr.s(auto_attribs=True)
class UserPermission:
    """ Details of a permission and its availability to a user. """

    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    type: Union[Unset, UserPermissionType] = UNSET
    description: Union[Unset, str] = UNSET
    have_permission: Union[Unset, bool] = UNSET
    deprecated_key: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        key = self.key
        name = self.name
        type: Union[Unset, UserPermissionType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        description = self.description
        have_permission = self.have_permission
        deprecated_key = self.deprecated_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if have_permission is not UNSET:
            field_dict["havePermission"] = have_permission
        if deprecated_key is not UNSET:
            field_dict["deprecatedKey"] = deprecated_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        type: Union[Unset, UserPermissionType] = UNSET
        _type = d.pop("type", UNSET)
        if not isinstance(_type, Unset):
            type = UserPermissionType(_type)

        description = d.pop("description", UNSET)

        have_permission = d.pop("havePermission", UNSET)

        deprecated_key = d.pop("deprecatedKey", UNSET)

        user_permission = cls(
            id=id,
            key=key,
            name=name,
            type=type,
            description=description,
            have_permission=have_permission,
            deprecated_key=deprecated_key,
        )

        user_permission.additional_properties = d
        return user_permission

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
