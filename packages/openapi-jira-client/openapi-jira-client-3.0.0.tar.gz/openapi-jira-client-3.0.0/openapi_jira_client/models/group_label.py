from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.group_label_type import GroupLabelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupLabel")


@attr.s(auto_attribs=True)
class GroupLabel:
    """ A group label. """

    text: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    type: Union[Unset, GroupLabelType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        title = self.title
        type: Union[Unset, GroupLabelType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if text is not UNSET:
            field_dict["text"] = text
        if title is not UNSET:
            field_dict["title"] = title
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text", UNSET)

        title = d.pop("title", UNSET)

        type: Union[Unset, GroupLabelType] = UNSET
        _type = d.pop("type", UNSET)
        if not isinstance(_type, Unset):
            type = GroupLabelType(_type)

        group_label = cls(
            text=text,
            title=title,
            type=type,
        )

        return group_label
