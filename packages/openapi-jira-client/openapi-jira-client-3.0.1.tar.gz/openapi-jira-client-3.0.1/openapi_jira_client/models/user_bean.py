from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserBean")


@attr.s(auto_attribs=True)
class UserBean:
    """  """

    key: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    account_id: Union[Unset, str] = UNSET
    avatar_urls: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        self_ = self.self_
        name = self.name
        display_name = self.display_name
        active = self.active
        account_id = self.account_id
        avatar_urls = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if self_ is not UNSET:
            field_dict["self"] = self_
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if active is not UNSET:
            field_dict["active"] = active
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        self_ = d.pop("self", UNSET)

        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        active = d.pop("active", UNSET)

        account_id = d.pop("accountId", UNSET)

        avatar_urls = None

        user_bean = cls(
            key=key,
            self_=self_,
            name=name,
            display_name=display_name,
            active=active,
            account_id=account_id,
            avatar_urls=avatar_urls,
        )

        return user_bean
