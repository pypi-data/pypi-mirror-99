from typing import Any, Dict, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectIdentifiers")


@attr.s(auto_attribs=True)
class ProjectIdentifiers:
    """ Identifiers for a project. """

    self_: str
    id: int
    key: str

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id = self.id
        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "self": self_,
                "id": id,
                "key": key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self")

        id = d.pop("id")

        key = d.pop("key")

        project_identifiers = cls(
            self_=self_,
            id=id,
            key=key,
        )

        return project_identifiers
