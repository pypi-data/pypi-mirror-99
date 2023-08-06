from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.security_level import SecurityLevel
from ..types import UNSET, Unset

T = TypeVar("T", bound="SecurityScheme")


@attr.s(auto_attribs=True)
class SecurityScheme:
    """ Details about a security scheme. """

    self_: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    default_security_level_id: Union[Unset, int] = UNSET
    levels: Union[Unset, List[SecurityLevel]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id = self.id
        name = self.name
        description = self.description
        default_security_level_id = self.default_security_level_id
        levels: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.levels, Unset):
            levels = []
            for levels_item_data in self.levels:
                levels_item = levels_item_data.to_dict()

                levels.append(levels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if default_security_level_id is not UNSET:
            field_dict["defaultSecurityLevelId"] = default_security_level_id
        if levels is not UNSET:
            field_dict["levels"] = levels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        default_security_level_id = d.pop("defaultSecurityLevelId", UNSET)

        levels = []
        _levels = d.pop("levels", UNSET)
        for levels_item_data in _levels or []:
            levels_item = SecurityLevel.from_dict(levels_item_data)

            levels.append(levels_item)

        security_scheme = cls(
            self_=self_,
            id=id,
            name=name,
            description=description,
            default_security_level_id=default_security_level_id,
            levels=levels,
        )

        return security_scheme
