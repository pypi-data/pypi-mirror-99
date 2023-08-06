from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScreenSchemeDetails")


@attr.s(auto_attribs=True)
class ScreenSchemeDetails:
    """ Details of a screen scheme. """

    name: str
    screens: None
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        screens = None

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "screens": screens,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        screens = None

        description = d.pop("description", UNSET)

        screen_scheme_details = cls(
            name=name,
            screens=screens,
            description=description,
        )

        return screen_scheme_details
