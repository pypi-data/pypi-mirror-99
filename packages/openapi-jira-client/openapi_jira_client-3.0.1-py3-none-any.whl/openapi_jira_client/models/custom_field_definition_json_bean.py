from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.custom_field_definition_json_bean_searcher_key import CustomFieldDefinitionJsonBeanSearcherKey
from ..models.custom_field_definition_json_bean_type import CustomFieldDefinitionJsonBeanType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldDefinitionJsonBean")


@attr.s(auto_attribs=True)
class CustomFieldDefinitionJsonBean:
    """  """

    name: str
    type_: CustomFieldDefinitionJsonBeanType
    searcher_key: CustomFieldDefinitionJsonBeanSearcherKey
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type_ = self.type_.value

        searcher_key = self.searcher_key.value

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "searcherKey": searcher_key,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type_ = CustomFieldDefinitionJsonBeanType(d.pop("type"))

        searcher_key = CustomFieldDefinitionJsonBeanSearcherKey(d.pop("searcherKey"))

        description = d.pop("description", UNSET)

        custom_field_definition_json_bean = cls(
            name=name,
            type_=type_,
            searcher_key=searcher_key,
            description=description,
        )

        return custom_field_definition_json_bean
