from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.jql_query_field_entity_property import JqlQueryFieldEntityProperty
from ..types import UNSET, Unset

T = TypeVar("T", bound="JqlQueryField")


@attr.s(auto_attribs=True)
class JqlQueryField:
    """ A field used in a JQL query. See [Advanced searching - fields reference](https://confluence.atlassian.com/x/dAiiLQ) for more information about fields in JQL queries. """

    name: str
    property: Union[Unset, List[JqlQueryFieldEntityProperty]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        property: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.property, Unset):
            property = []
            for property_item_data in self.property:
                property_item = property_item_data.to_dict()

                property.append(property_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if property is not UNSET:
            field_dict["property"] = property

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        property = []
        _property = d.pop("property", UNSET)
        for property_item_data in _property or []:
            property_item = JqlQueryFieldEntityProperty.from_dict(property_item_data)

            property.append(property_item)

        jql_query_field = cls(
            name=name,
            property=property,
        )

        return jql_query_field
