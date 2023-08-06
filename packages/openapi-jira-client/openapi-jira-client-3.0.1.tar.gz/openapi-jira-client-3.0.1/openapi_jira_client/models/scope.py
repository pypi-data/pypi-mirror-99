from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.scope_type import ScopeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Scope")


@attr.s(auto_attribs=True)
class Scope:
    """ The projects the item is associated with. Indicated for items associated with [next-gen projects](https://confluence.atlassian.com/x/loMyO). """

    type_: Union[Unset, ScopeType] = UNSET
    project: Union[Unset, None] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        project = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_: Union[Unset, ScopeType] = UNSET
        _type_ = d.pop("type", UNSET)
        if not isinstance(_type_, Unset):
            type_ = ScopeType(_type_)

        project = None

        scope = cls(
            type_=type_,
            project=project,
        )

        scope.additional_properties = d
        return scope

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
