from typing import Any, Dict, List, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRoles")


@attr.s(auto_attribs=True)
class ProjectRoles:
    """ The name and self URL for each role defined in the project. For more information, see [Create project role](#api-rest-api-3-role-post). """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_roles = cls()

        project_roles.additional_properties = d
        return project_roles

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
