from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.history_metadata_extra_data import HistoryMetadataExtraData
from ..types import UNSET, Unset

T = TypeVar("T", bound="HistoryMetadata")


@attr.s(auto_attribs=True)
class HistoryMetadata:
    """ Details of issue history metadata. """

    type_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    description_key: Union[Unset, str] = UNSET
    activity_description: Union[Unset, str] = UNSET
    activity_description_key: Union[Unset, str] = UNSET
    email_description: Union[Unset, str] = UNSET
    email_description_key: Union[Unset, str] = UNSET
    actor: Union[Unset, None] = UNSET
    generator: Union[Unset, None] = UNSET
    cause: Union[Unset, None] = UNSET
    extra_data: Union[Unset, HistoryMetadataExtraData] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type_ = self.type_
        description = self.description
        description_key = self.description_key
        activity_description = self.activity_description
        activity_description_key = self.activity_description_key
        email_description = self.email_description
        email_description_key = self.email_description_key
        actor = None

        generator = None

        cause = None

        extra_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_data, Unset):
            extra_data = self.extra_data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if description is not UNSET:
            field_dict["description"] = description
        if description_key is not UNSET:
            field_dict["descriptionKey"] = description_key
        if activity_description is not UNSET:
            field_dict["activityDescription"] = activity_description
        if activity_description_key is not UNSET:
            field_dict["activityDescriptionKey"] = activity_description_key
        if email_description is not UNSET:
            field_dict["emailDescription"] = email_description
        if email_description_key is not UNSET:
            field_dict["emailDescriptionKey"] = email_description_key
        if actor is not UNSET:
            field_dict["actor"] = actor
        if generator is not UNSET:
            field_dict["generator"] = generator
        if cause is not UNSET:
            field_dict["cause"] = cause
        if extra_data is not UNSET:
            field_dict["extraData"] = extra_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = d.pop("type", UNSET)

        description = d.pop("description", UNSET)

        description_key = d.pop("descriptionKey", UNSET)

        activity_description = d.pop("activityDescription", UNSET)

        activity_description_key = d.pop("activityDescriptionKey", UNSET)

        email_description = d.pop("emailDescription", UNSET)

        email_description_key = d.pop("emailDescriptionKey", UNSET)

        actor = None

        generator = None

        cause = None

        extra_data: Union[Unset, HistoryMetadataExtraData] = UNSET
        _extra_data = d.pop("extraData", UNSET)
        if not isinstance(_extra_data, Unset):
            extra_data = HistoryMetadataExtraData.from_dict(_extra_data)

        history_metadata = cls(
            type_=type_,
            description=description,
            description_key=description_key,
            activity_description=activity_description,
            activity_description_key=activity_description_key,
            email_description=email_description,
            email_description_key=email_description_key,
            actor=actor,
            generator=generator,
            cause=cause,
            extra_data=extra_data,
        )

        history_metadata.additional_properties = d
        return history_metadata

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
