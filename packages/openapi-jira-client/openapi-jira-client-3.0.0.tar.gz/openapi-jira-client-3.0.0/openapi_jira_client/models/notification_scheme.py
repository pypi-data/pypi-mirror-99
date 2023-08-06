from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.notification_scheme_event import NotificationSchemeEvent
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationScheme")


@attr.s(auto_attribs=True)
class NotificationScheme:
    """ Details about a notification scheme. """

    expand: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    notification_scheme_events: Union[Unset, List[NotificationSchemeEvent]] = UNSET
    scope: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        id = self.id
        self_ = self.self_
        name = self.name
        description = self.description
        notification_scheme_events: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.notification_scheme_events, Unset):
            notification_scheme_events = []
            for notification_scheme_events_item_data in self.notification_scheme_events:
                notification_scheme_events_item = notification_scheme_events_item_data.to_dict()

                notification_scheme_events.append(notification_scheme_events_item)

        scope = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if id is not UNSET:
            field_dict["id"] = id
        if self_ is not UNSET:
            field_dict["self"] = self_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if notification_scheme_events is not UNSET:
            field_dict["notificationSchemeEvents"] = notification_scheme_events
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        id = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        notification_scheme_events = []
        _notification_scheme_events = d.pop("notificationSchemeEvents", UNSET)
        for notification_scheme_events_item_data in _notification_scheme_events or []:
            notification_scheme_events_item = NotificationSchemeEvent.from_dict(notification_scheme_events_item_data)

            notification_scheme_events.append(notification_scheme_events_item)

        scope = None

        notification_scheme = cls(
            expand=expand,
            id=id,
            self_=self_,
            name=name,
            description=description,
            notification_scheme_events=notification_scheme_events,
            scope=scope,
        )

        return notification_scheme
