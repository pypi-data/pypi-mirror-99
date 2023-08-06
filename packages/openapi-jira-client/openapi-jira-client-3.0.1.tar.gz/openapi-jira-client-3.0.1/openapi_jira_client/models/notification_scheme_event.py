from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.event_notification import EventNotification
from ..models.notification_event import NotificationEvent
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationSchemeEvent")


@attr.s(auto_attribs=True)
class NotificationSchemeEvent:
    """ Details about a notification scheme event. """

    event: Union[Unset, NotificationEvent] = UNSET
    notifications: Union[Unset, List[EventNotification]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        event: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.event, Unset):
            event = self.event.to_dict()

        notifications: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.notifications, Unset):
            notifications = []
            for notifications_item_data in self.notifications:
                notifications_item = notifications_item_data.to_dict()

                notifications.append(notifications_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if event is not UNSET:
            field_dict["event"] = event
        if notifications is not UNSET:
            field_dict["notifications"] = notifications

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        event: Union[Unset, NotificationEvent] = UNSET
        _event = d.pop("event", UNSET)
        if not isinstance(_event, Unset):
            event = NotificationEvent.from_dict(_event)

        notifications = []
        _notifications = d.pop("notifications", UNSET)
        for notifications_item_data in _notifications or []:
            notifications_item = EventNotification.from_dict(notifications_item_data)

            notifications.append(notifications_item)

        notification_scheme_event = cls(
            event=event,
            notifications=notifications,
        )

        return notification_scheme_event
