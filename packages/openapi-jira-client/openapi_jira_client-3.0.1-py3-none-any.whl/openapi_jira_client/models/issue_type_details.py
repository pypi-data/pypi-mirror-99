from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeDetails")


@attr.s(auto_attribs=True)
class IssueTypeDetails:
    """ Details about an issue type. """

    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    icon_url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    subtask: Union[Unset, bool] = UNSET
    avatar_id: Union[Unset, int] = UNSET
    entity_id: Union[Unset, str] = UNSET
    hierarchy_level: Union[Unset, int] = UNSET
    scope: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        description = self.description
        icon_url = self.icon_url
        name = self.name
        subtask = self.subtask
        avatar_id = self.avatar_id
        entity_id = self.entity_id
        hierarchy_level = self.hierarchy_level
        scope = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if description is not UNSET:
            field_dict["description"] = description
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url
        if name is not UNSET:
            field_dict["name"] = name
        if subtask is not UNSET:
            field_dict["subtask"] = subtask
        if avatar_id is not UNSET:
            field_dict["avatarId"] = avatar_id
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if hierarchy_level is not UNSET:
            field_dict["hierarchyLevel"] = hierarchy_level
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        icon_url = d.pop("iconUrl", UNSET)

        name = d.pop("name", UNSET)

        subtask = d.pop("subtask", UNSET)

        avatar_id = d.pop("avatarId", UNSET)

        entity_id = d.pop("entityId", UNSET)

        hierarchy_level = d.pop("hierarchyLevel", UNSET)

        scope = None

        issue_type_details = cls(
            self_=self_,
            id_=id_,
            description=description,
            icon_url=icon_url,
            name=name,
            subtask=subtask,
            avatar_id=avatar_id,
            entity_id=entity_id,
            hierarchy_level=hierarchy_level,
            scope=scope,
        )

        return issue_type_details
