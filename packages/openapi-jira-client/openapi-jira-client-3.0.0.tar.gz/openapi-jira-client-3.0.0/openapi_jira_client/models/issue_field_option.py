from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.issue_field_option_configuration import IssueFieldOptionConfiguration
from ..models.issue_field_option_properties import IssueFieldOptionProperties
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueFieldOption")


@attr.s(auto_attribs=True)
class IssueFieldOption:
    """ Details of the options for a select list issue field. """

    id: int
    value: str
    properties: Union[IssueFieldOptionProperties, Unset] = UNSET
    config: Union[IssueFieldOptionConfiguration, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        value = self.value
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if properties is not UNSET:
            field_dict["properties"] = properties
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        properties: Union[IssueFieldOptionProperties, Unset] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = IssueFieldOptionProperties.from_dict(_properties)

        config: Union[IssueFieldOptionConfiguration, Unset] = UNSET
        _config = d.pop("config", UNSET)
        if not isinstance(_config, Unset):
            config = IssueFieldOptionConfiguration.from_dict(_config)

        issue_field_option = cls(
            id=id,
            value=value,
            properties=properties,
            config=config,
        )

        return issue_field_option
