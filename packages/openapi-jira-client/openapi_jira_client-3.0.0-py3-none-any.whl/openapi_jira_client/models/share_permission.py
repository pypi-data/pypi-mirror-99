from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.share_permission_type import SharePermissionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SharePermission")


@attr.s(auto_attribs=True)
class SharePermission:
    """ Details of a share permission for the filter. """

    type: SharePermissionType
    id: Union[Unset, int] = UNSET
    project: Union[Unset, None] = UNSET
    role: Union[Unset, None] = UNSET
    group: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id
        project = None

        role = None

        group = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if project is not UNSET:
            field_dict["project"] = project
        if role is not UNSET:
            field_dict["role"] = role
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = SharePermissionType(d.pop("type"))

        id = d.pop("id", UNSET)

        project = None

        role = None

        group = None

        share_permission = cls(
            type=type,
            id=id,
            project=project,
            role=role,
            group=group,
        )

        return share_permission
