from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScreenWithTab")


@attr.s(auto_attribs=True)
class ScreenWithTab:
    """ A screen with tab details. """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    scope: Union[Unset, None] = UNSET
    tab: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        scope = None

        tab = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if scope is not UNSET:
            field_dict["scope"] = scope
        if tab is not UNSET:
            field_dict["tab"] = tab

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        scope = None

        tab = None

        screen_with_tab = cls(
            id_=id_,
            name=name,
            description=description,
            scope=scope,
            tab=tab,
        )

        return screen_with_tab
