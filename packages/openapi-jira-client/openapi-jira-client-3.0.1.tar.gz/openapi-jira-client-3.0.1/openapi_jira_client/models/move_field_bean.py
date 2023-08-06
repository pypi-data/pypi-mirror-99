from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.move_field_bean_position import MoveFieldBeanPosition
from ..types import UNSET, Unset

T = TypeVar("T", bound="MoveFieldBean")


@attr.s(auto_attribs=True)
class MoveFieldBean:
    """  """

    after: Union[Unset, str] = UNSET
    position: Union[Unset, MoveFieldBeanPosition] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        after = self.after
        position: Union[Unset, str] = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if after is not UNSET:
            field_dict["after"] = after
        if position is not UNSET:
            field_dict["position"] = position

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        after = d.pop("after", UNSET)

        position: Union[Unset, MoveFieldBeanPosition] = UNSET
        _position = d.pop("position", UNSET)
        if not isinstance(_position, Unset):
            position = MoveFieldBeanPosition(_position)

        move_field_bean = cls(
            after=after,
            position=position,
        )

        return move_field_bean
