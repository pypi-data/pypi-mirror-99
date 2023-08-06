from typing import Any, Dict, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeScreenSchemeId")


@attr.s(auto_attribs=True)
class IssueTypeScreenSchemeId:
    """ The ID of an issue type screen scheme. """

    id: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        issue_type_screen_scheme_id = cls(
            id=id,
        )

        return issue_type_screen_scheme_id
