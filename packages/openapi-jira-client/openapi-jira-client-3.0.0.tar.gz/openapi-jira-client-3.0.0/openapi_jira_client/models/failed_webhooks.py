from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.failed_webhook import FailedWebhook
from ..types import UNSET, Unset

T = TypeVar("T", bound="FailedWebhooks")


@attr.s(auto_attribs=True)
class FailedWebhooks:
    """ A page of failed webhooks. """

    values: List[FailedWebhook]
    max_results: int
    next: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()

            values.append(values_item)

        max_results = self.max_results
        next = self.next

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "values": values,
                "maxResults": max_results,
            }
        )
        if next is not UNSET:
            field_dict["next"] = next

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = FailedWebhook.from_dict(values_item_data)

            values.append(values_item)

        max_results = d.pop("maxResults")

        next = d.pop("next", UNSET)

        failed_webhooks = cls(
            values=values,
            max_results=max_results,
            next=next,
        )

        return failed_webhooks
