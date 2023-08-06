from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.json_node import JsonNode
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueEntityPropertiesProperties")


@attr.s(auto_attribs=True)
class IssueEntityPropertiesProperties:
    """ A list of entity property keys and values. """

    additional_properties: Dict[str, JsonNode] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_entity_properties_properties = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = JsonNode.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        issue_entity_properties_properties.additional_properties = additional_properties
        return issue_entity_properties_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> JsonNode:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: JsonNode) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
