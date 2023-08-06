from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationEvent")


@attr.s(auto_attribs=True)
class NotificationEvent:
    """ Details about a notification event. """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    template_event: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        template_event = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if template_event is not UNSET:
            field_dict["templateEvent"] = template_event

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        template_event = None

        notification_event = cls(
            id_=id_,
            name=name,
            description=description,
            template_event=template_event,
        )

        return notification_event
