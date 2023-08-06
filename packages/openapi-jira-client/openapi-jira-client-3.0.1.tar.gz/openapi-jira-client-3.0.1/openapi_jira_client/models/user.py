from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.user_account_type import UserAccountType
from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@attr.s(auto_attribs=True)
class User:
    """A user with details as permitted by the user's Atlassian Account privacy settings. However, be aware of these exceptions:

    *  User record deleted from Atlassian: This occurs as the result of a right to be forgotten request. In this case, `displayName` provides an indication and other parameters have default values or are blank (for example, email is blank).
    *  User record corrupted: This occurs as a results of events such as a server import and can only happen to deleted users. In this case, `accountId` returns *unknown* and all other parameters have fallback values.
    *  User record unavailable: This usually occurs due to an internal service outage. In this case, all parameters have fallback values."""

    self_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    account_id: Union[Unset, str] = UNSET
    account_type: Union[Unset, UserAccountType] = UNSET
    name: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    avatar_urls: Union[Unset, None] = UNSET
    display_name: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    time_zone: Union[Unset, str] = UNSET
    locale: Union[Unset, str] = UNSET
    groups: Union[Unset, None] = UNSET
    application_roles: Union[Unset, None] = UNSET
    expand: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        key = self.key
        account_id = self.account_id
        account_type: Union[Unset, str] = UNSET
        if not isinstance(self.account_type, Unset):
            account_type = self.account_type.value

        name = self.name
        email_address = self.email_address
        avatar_urls = None

        display_name = self.display_name
        active = self.active
        time_zone = self.time_zone
        locale = self.locale
        groups = None

        application_roles = None

        expand = self.expand

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if key is not UNSET:
            field_dict["key"] = key
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if account_type is not UNSET:
            field_dict["accountType"] = account_type
        if name is not UNSET:
            field_dict["name"] = name
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if active is not UNSET:
            field_dict["active"] = active
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if locale is not UNSET:
            field_dict["locale"] = locale
        if groups is not UNSET:
            field_dict["groups"] = groups
        if application_roles is not UNSET:
            field_dict["applicationRoles"] = application_roles
        if expand is not UNSET:
            field_dict["expand"] = expand

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        key = d.pop("key", UNSET)

        account_id = d.pop("accountId", UNSET)

        account_type: Union[Unset, UserAccountType] = UNSET
        _account_type = d.pop("accountType", UNSET)
        if not isinstance(_account_type, Unset):
            account_type = UserAccountType(_account_type)

        name = d.pop("name", UNSET)

        email_address = d.pop("emailAddress", UNSET)

        avatar_urls = None

        display_name = d.pop("displayName", UNSET)

        active = d.pop("active", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        locale = d.pop("locale", UNSET)

        groups = None

        application_roles = None

        expand = d.pop("expand", UNSET)

        user = cls(
            self_=self_,
            key=key,
            account_id=account_id,
            account_type=account_type,
            name=name,
            email_address=email_address,
            avatar_urls=avatar_urls,
            display_name=display_name,
            active=active,
            time_zone=time_zone,
            locale=locale,
            groups=groups,
            application_roles=application_roles,
            expand=expand,
        )

        return user
