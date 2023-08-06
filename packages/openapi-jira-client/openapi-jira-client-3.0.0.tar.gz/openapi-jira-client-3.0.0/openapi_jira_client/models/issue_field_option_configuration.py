from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.issue_field_option_configuration_attributes_item import IssueFieldOptionConfigurationAttributesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueFieldOptionConfiguration")


@attr.s(auto_attribs=True)
class IssueFieldOptionConfiguration:
    """ Details of the projects the option is available in. """

    scope: Union[Unset, None] = UNSET
    attributes: Union[Unset, List[IssueFieldOptionConfigurationAttributesItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        scope = None

        attributes: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = []
            for attributes_item_data in self.attributes:
                attributes_item = attributes_item_data.value

                attributes.append(attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if scope is not UNSET:
            field_dict["scope"] = scope
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scope = None

        attributes = []
        _attributes = d.pop("attributes", UNSET)
        for attributes_item_data in _attributes or []:
            attributes_item = IssueFieldOptionConfigurationAttributesItem(attributes_item_data)

            attributes.append(attributes_item)

        issue_field_option_configuration = cls(
            scope=scope,
            attributes=attributes,
        )

        return issue_field_option_configuration
