from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.issue_type_issue_create_metadata import IssueTypeIssueCreateMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectIssueCreateMetadata")


@attr.s(auto_attribs=True)
class ProjectIssueCreateMetadata:
    """ Details of the issue creation metadata for a project. """

    expand: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    avatar_urls: Union[Unset, None] = UNSET
    issuetypes: Union[Unset, List[IssueTypeIssueCreateMetadata]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        self_ = self.self_
        id = self.id
        key = self.key
        name = self.name
        avatar_urls = None

        issuetypes: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.issuetypes, Unset):
            issuetypes = []
            for issuetypes_item_data in self.issuetypes:
                issuetypes_item = issuetypes_item_data.to_dict()

                issuetypes.append(issuetypes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if issuetypes is not UNSET:
            field_dict["issuetypes"] = issuetypes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        self_ = d.pop("self", UNSET)

        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        avatar_urls = None

        issuetypes = []
        _issuetypes = d.pop("issuetypes", UNSET)
        for issuetypes_item_data in _issuetypes or []:
            issuetypes_item = IssueTypeIssueCreateMetadata.from_dict(issuetypes_item_data)

            issuetypes.append(issuetypes_item)

        project_issue_create_metadata = cls(
            expand=expand,
            self_=self_,
            id=id,
            key=key,
            name=name,
            avatar_urls=avatar_urls,
            issuetypes=issuetypes,
        )

        return project_issue_create_metadata
