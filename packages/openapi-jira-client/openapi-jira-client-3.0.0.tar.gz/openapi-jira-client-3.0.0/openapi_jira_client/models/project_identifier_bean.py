from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectIdentifierBean")


@attr.s(auto_attribs=True)
class ProjectIdentifierBean:
    """ The identifiers for a project. """

    id: Union[Unset, int] = UNSET
    key: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        project_identifier_bean = cls(
            id=id,
            key=key,
        )

        return project_identifier_bean
