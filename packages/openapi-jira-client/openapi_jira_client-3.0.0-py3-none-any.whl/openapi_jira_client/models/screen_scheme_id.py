from typing import Any, Dict, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScreenSchemeId")


@attr.s(auto_attribs=True)
class ScreenSchemeId:
    """ The ID of a screen scheme. """

    id: int

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

        screen_scheme_id = cls(
            id=id,
        )

        return screen_scheme_id
