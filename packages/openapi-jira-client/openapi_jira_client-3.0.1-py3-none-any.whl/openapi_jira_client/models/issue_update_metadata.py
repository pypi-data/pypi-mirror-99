from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.issue_update_metadata_fields import IssueUpdateMetadataFields
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueUpdateMetadata")


@attr.s(auto_attribs=True)
class IssueUpdateMetadata:
    """ A list of editable field details. """

    fields: Union[Unset, IssueUpdateMetadataFields] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields: Union[Unset, IssueUpdateMetadataFields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = IssueUpdateMetadataFields.from_dict(_fields)

        issue_update_metadata = cls(
            fields=fields,
        )

        issue_update_metadata.additional_properties = d
        return issue_update_metadata

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
