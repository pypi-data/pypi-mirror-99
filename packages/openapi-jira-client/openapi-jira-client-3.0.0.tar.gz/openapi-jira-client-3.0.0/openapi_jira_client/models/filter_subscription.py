from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterSubscription")


@attr.s(auto_attribs=True)
class FilterSubscription:
    """ Details of a user or group subscribing to a filter. """

    id: Union[Unset, int] = UNSET
    user: Union[Unset, None] = UNSET
    group: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        user = None

        group = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if user is not UNSET:
            field_dict["user"] = user
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        user = None

        group = None

        filter_subscription = cls(
            id=id,
            user=user,
            group=group,
        )

        return filter_subscription
