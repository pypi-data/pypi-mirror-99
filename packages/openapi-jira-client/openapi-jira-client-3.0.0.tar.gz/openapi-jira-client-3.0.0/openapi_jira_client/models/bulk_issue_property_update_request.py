from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkIssuePropertyUpdateRequest")


@attr.s(auto_attribs=True)
class BulkIssuePropertyUpdateRequest:
    """ Bulk issue property update request details. """

    value: Union[Unset, None] = UNSET
    expression: Union[Unset, str] = UNSET
    filter: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = None

        expression = self.expression
        filter = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if expression is not UNSET:
            field_dict["expression"] = expression
        if filter is not UNSET:
            field_dict["filter"] = filter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = None

        expression = d.pop("expression", UNSET)

        filter = None

        bulk_issue_property_update_request = cls(
            value=value,
            expression=expression,
            filter=filter,
        )

        return bulk_issue_property_update_request
