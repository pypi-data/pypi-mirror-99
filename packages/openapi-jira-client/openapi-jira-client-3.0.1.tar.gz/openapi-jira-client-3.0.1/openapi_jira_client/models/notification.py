from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Notification")


@attr.s(auto_attribs=True)
class Notification:
    """ Details about a notification. """

    subject: Union[Unset, str] = UNSET
    text_body: Union[Unset, str] = UNSET
    html_body: Union[Unset, str] = UNSET
    to: Union[Unset, None] = UNSET
    restrict: Union[Unset, None] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject = self.subject
        text_body = self.text_body
        html_body = self.html_body
        to = None

        restrict = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subject is not UNSET:
            field_dict["subject"] = subject
        if text_body is not UNSET:
            field_dict["textBody"] = text_body
        if html_body is not UNSET:
            field_dict["htmlBody"] = html_body
        if to is not UNSET:
            field_dict["to"] = to
        if restrict is not UNSET:
            field_dict["restrict"] = restrict

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subject = d.pop("subject", UNSET)

        text_body = d.pop("textBody", UNSET)

        html_body = d.pop("htmlBody", UNSET)

        to = None

        restrict = None

        notification = cls(
            subject=subject,
            text_body=text_body,
            html_body=html_body,
            to=to,
            restrict=restrict,
        )

        notification.additional_properties = d
        return notification

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
