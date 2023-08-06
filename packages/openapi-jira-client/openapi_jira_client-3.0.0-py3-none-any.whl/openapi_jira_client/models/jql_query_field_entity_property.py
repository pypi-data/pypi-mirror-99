from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.jql_query_field_entity_property_type import JqlQueryFieldEntityPropertyType
from ..types import UNSET, Unset

T = TypeVar("T", bound="JqlQueryFieldEntityProperty")


@attr.s(auto_attribs=True)
class JqlQueryFieldEntityProperty:
    """ Details of an entity property. """

    entity: str
    key: str
    path: str
    type: Union[Unset, JqlQueryFieldEntityPropertyType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity = self.entity
        key = self.key
        path = self.path
        type: Union[Unset, JqlQueryFieldEntityPropertyType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity": entity,
                "key": key,
                "path": path,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity = d.pop("entity")

        key = d.pop("key")

        path = d.pop("path")

        type: Union[Unset, JqlQueryFieldEntityPropertyType] = UNSET
        _type = d.pop("type", UNSET)
        if not isinstance(_type, Unset):
            type = JqlQueryFieldEntityPropertyType(_type)

        jql_query_field_entity_property = cls(
            entity=entity,
            key=key,
            path=path,
            type=type,
        )

        jql_query_field_entity_property.additional_properties = d
        return jql_query_field_entity_property

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
