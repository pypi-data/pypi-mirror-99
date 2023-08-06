from typing import Any, Dict, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IdBean")


@attr.s(auto_attribs=True)
class IdBean:
    """  """

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

        id_bean = cls(
            id=id,
        )

        return id_bean
