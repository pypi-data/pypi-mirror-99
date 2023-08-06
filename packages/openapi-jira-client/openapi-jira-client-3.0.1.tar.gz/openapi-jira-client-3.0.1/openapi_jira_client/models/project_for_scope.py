from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.project_for_scope_project_type_key import ProjectForScopeProjectTypeKey
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectForScope")


@attr.s(auto_attribs=True)
class ProjectForScope:
    """ Details about a next-gen project. """

    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    project_type_key: Union[Unset, ProjectForScopeProjectTypeKey] = UNSET
    simplified: Union[Unset, bool] = UNSET
    avatar_urls: Union[Unset, None] = UNSET
    project_category: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        key = self.key
        name = self.name
        project_type_key: Union[Unset, str] = UNSET
        if not isinstance(self.project_type_key, Unset):
            project_type_key = self.project_type_key.value

        simplified = self.simplified
        avatar_urls = None

        project_category = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if project_type_key is not UNSET:
            field_dict["projectTypeKey"] = project_type_key
        if simplified is not UNSET:
            field_dict["simplified"] = simplified
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if project_category is not UNSET:
            field_dict["projectCategory"] = project_category

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        project_type_key: Union[Unset, ProjectForScopeProjectTypeKey] = UNSET
        _project_type_key = d.pop("projectTypeKey", UNSET)
        if not isinstance(_project_type_key, Unset):
            project_type_key = ProjectForScopeProjectTypeKey(_project_type_key)

        simplified = d.pop("simplified", UNSET)

        avatar_urls = None

        project_category = None

        project_for_scope = cls(
            self_=self_,
            id_=id_,
            key=key,
            name=name,
            project_type_key=project_type_key,
            simplified=simplified,
            avatar_urls=avatar_urls,
            project_category=project_category,
        )

        return project_for_scope
