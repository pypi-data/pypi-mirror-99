from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldConfigurationScheme")


@attr.s(auto_attribs=True)
class FieldConfigurationScheme:
    """ Details of a field configuration scheme. """

    id: str
    name: str
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        field_configuration_scheme = cls(
            id=id,
            name=name,
            description=description,
        )

        return field_configuration_scheme
