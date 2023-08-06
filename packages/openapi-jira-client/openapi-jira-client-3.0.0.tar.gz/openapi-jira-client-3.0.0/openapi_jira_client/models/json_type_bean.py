from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.json_type_bean_configuration import JsonTypeBeanConfiguration
from ..types import UNSET, Unset

T = TypeVar("T", bound="JsonTypeBean")


@attr.s(auto_attribs=True)
class JsonTypeBean:
    """ The schema of a field. """

    type: str
    items: Union[Unset, str] = UNSET
    system: Union[Unset, str] = UNSET
    custom: Union[Unset, str] = UNSET
    custom_id: Union[Unset, int] = UNSET
    configuration: Union[JsonTypeBeanConfiguration, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        items = self.items
        system = self.system
        custom = self.custom
        custom_id = self.custom_id
        configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
            }
        )
        if items is not UNSET:
            field_dict["items"] = items
        if system is not UNSET:
            field_dict["system"] = system
        if custom is not UNSET:
            field_dict["custom"] = custom
        if custom_id is not UNSET:
            field_dict["customId"] = custom_id
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        items = d.pop("items", UNSET)

        system = d.pop("system", UNSET)

        custom = d.pop("custom", UNSET)

        custom_id = d.pop("customId", UNSET)

        configuration: Union[JsonTypeBeanConfiguration, Unset] = UNSET
        _configuration = d.pop("configuration", UNSET)
        if not isinstance(_configuration, Unset):
            configuration = JsonTypeBeanConfiguration.from_dict(_configuration)

        json_type_bean = cls(
            type=type,
            items=items,
            system=system,
            custom=custom,
            custom_id=custom_id,
            configuration=configuration,
        )

        return json_type_bean
