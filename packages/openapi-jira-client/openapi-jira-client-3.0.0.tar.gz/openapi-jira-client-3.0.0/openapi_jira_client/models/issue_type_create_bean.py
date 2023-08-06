from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.issue_type_create_bean_type import IssueTypeCreateBeanType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeCreateBean")


@attr.s(auto_attribs=True)
class IssueTypeCreateBean:
    """  """

    name: str
    description: Union[Unset, str] = UNSET
    type: Union[Unset, IssueTypeCreateBeanType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        type: Union[Unset, IssueTypeCreateBeanType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description", UNSET)

        type: Union[Unset, IssueTypeCreateBeanType] = UNSET
        _type = d.pop("type", UNSET)
        if not isinstance(_type, Unset):
            type = IssueTypeCreateBeanType(_type)

        issue_type_create_bean = cls(
            name=name,
            description=description,
            type=type,
        )

        return issue_type_create_bean
