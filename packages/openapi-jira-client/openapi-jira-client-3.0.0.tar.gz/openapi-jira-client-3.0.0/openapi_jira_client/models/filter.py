from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.share_permission import SharePermission
from ..types import UNSET, Unset

T = TypeVar("T", bound="Filter")


@attr.s(auto_attribs=True)
class Filter:
    """ Details about a filter. """

    name: str
    self_: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    owner: Union[Unset, None] = UNSET
    jql: Union[Unset, str] = UNSET
    view_url: Union[Unset, str] = UNSET
    search_url: Union[Unset, str] = UNSET
    favourite: Union[Unset, bool] = UNSET
    favourited_count: Union[Unset, int] = UNSET
    share_permissions: Union[Unset, List[SharePermission]] = UNSET
    shared_users: Union[Unset, None] = UNSET
    subscriptions: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        self_ = self.self_
        id = self.id
        description = self.description
        owner = None

        jql = self.jql
        view_url = self.view_url
        search_url = self.search_url
        favourite = self.favourite
        favourited_count = self.favourited_count
        share_permissions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.share_permissions, Unset):
            share_permissions = []
            for share_permissions_item_data in self.share_permissions:
                share_permissions_item = share_permissions_item_data.to_dict()

                share_permissions.append(share_permissions_item)

        shared_users = None

        subscriptions = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if owner is not UNSET:
            field_dict["owner"] = owner
        if jql is not UNSET:
            field_dict["jql"] = jql
        if view_url is not UNSET:
            field_dict["viewUrl"] = view_url
        if search_url is not UNSET:
            field_dict["searchUrl"] = search_url
        if favourite is not UNSET:
            field_dict["favourite"] = favourite
        if favourited_count is not UNSET:
            field_dict["favouritedCount"] = favourited_count
        if share_permissions is not UNSET:
            field_dict["sharePermissions"] = share_permissions
        if shared_users is not UNSET:
            field_dict["sharedUsers"] = shared_users
        if subscriptions is not UNSET:
            field_dict["subscriptions"] = subscriptions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        self_ = d.pop("self", UNSET)

        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        owner = None

        jql = d.pop("jql", UNSET)

        view_url = d.pop("viewUrl", UNSET)

        search_url = d.pop("searchUrl", UNSET)

        favourite = d.pop("favourite", UNSET)

        favourited_count = d.pop("favouritedCount", UNSET)

        share_permissions = []
        _share_permissions = d.pop("sharePermissions", UNSET)
        for share_permissions_item_data in _share_permissions or []:
            share_permissions_item = SharePermission.from_dict(share_permissions_item_data)

            share_permissions.append(share_permissions_item)

        shared_users = None

        subscriptions = None

        filter = cls(
            name=name,
            self_=self_,
            id=id,
            description=description,
            owner=owner,
            jql=jql,
            view_url=view_url,
            search_url=search_url,
            favourite=favourite,
            favourited_count=favourited_count,
            share_permissions=share_permissions,
            shared_users=shared_users,
            subscriptions=subscriptions,
        )

        return filter
