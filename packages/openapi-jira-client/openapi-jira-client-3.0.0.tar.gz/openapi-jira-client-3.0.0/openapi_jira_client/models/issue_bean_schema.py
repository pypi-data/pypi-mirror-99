from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.json_type_bean import JsonTypeBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueBeanSchema")


@attr.s(auto_attribs=True)
class IssueBeanSchema:
    """ The schema describing each field present on the issue. """

    additional_properties: Dict[str, JsonTypeBean] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_bean_schema = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = JsonTypeBean.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        issue_bean_schema.additional_properties = additional_properties
        return issue_bean_schema

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> JsonTypeBean:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: JsonTypeBean) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
