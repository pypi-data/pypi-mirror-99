from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.webhook_events_item import WebhookEventsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Webhook")


@attr.s(auto_attribs=True)
class Webhook:
    """ A webhook. """

    id_: int
    jql_filter: str
    events: List[WebhookEventsItem]
    expiration_date: int

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        jql_filter = self.jql_filter
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.value

            events.append(events_item)

        expiration_date = self.expiration_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "jqlFilter": jql_filter,
                "events": events,
                "expirationDate": expiration_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        jql_filter = d.pop("jqlFilter")

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = WebhookEventsItem(events_item_data)

            events.append(events_item)

        expiration_date = d.pop("expirationDate")

        webhook = cls(
            id_=id_,
            jql_filter=jql_filter,
            events=events,
            expiration_date=expiration_date,
        )

        return webhook
