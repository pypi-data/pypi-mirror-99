from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.event_notification_notification_type import EventNotificationNotificationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EventNotification")


@attr.s(auto_attribs=True)
class EventNotification:
    """ Details about a notification associated with an event. """

    expand: Union[Unset, str] = UNSET
    id_: Union[Unset, int] = UNSET
    notification_type: Union[Unset, EventNotificationNotificationType] = UNSET
    parameter: Union[Unset, str] = UNSET
    group: Union[Unset, None] = UNSET
    field: Union[Unset, None] = UNSET
    email_address: Union[Unset, str] = UNSET
    project_role: Union[Unset, None] = UNSET
    user: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        id_ = self.id_
        notification_type: Union[Unset, str] = UNSET
        if not isinstance(self.notification_type, Unset):
            notification_type = self.notification_type.value

        parameter = self.parameter
        group = None

        field = None

        email_address = self.email_address
        project_role = None

        user = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if id_ is not UNSET:
            field_dict["id"] = id_
        if notification_type is not UNSET:
            field_dict["notificationType"] = notification_type
        if parameter is not UNSET:
            field_dict["parameter"] = parameter
        if group is not UNSET:
            field_dict["group"] = group
        if field is not UNSET:
            field_dict["field"] = field
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if project_role is not UNSET:
            field_dict["projectRole"] = project_role
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        id_ = d.pop("id", UNSET)

        notification_type: Union[Unset, EventNotificationNotificationType] = UNSET
        _notification_type = d.pop("notificationType", UNSET)
        if not isinstance(_notification_type, Unset):
            notification_type = EventNotificationNotificationType(_notification_type)

        parameter = d.pop("parameter", UNSET)

        group = None

        field = None

        email_address = d.pop("emailAddress", UNSET)

        project_role = None

        user = None

        event_notification = cls(
            expand=expand,
            id_=id_,
            notification_type=notification_type,
            parameter=parameter,
            group=group,
            field=field,
            email_address=email_address,
            project_role=project_role,
            user=user,
        )

        return event_notification
