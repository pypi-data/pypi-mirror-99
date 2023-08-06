from typing import Any, Dict, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScreenSchemeId")


@attr.s(auto_attribs=True)
class ScreenSchemeId:
    """ The ID of a screen scheme. """

    id_: int

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        screen_scheme_id = cls(
            id_=id_,
        )

        return screen_scheme_id
