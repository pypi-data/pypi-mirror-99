from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteIssueLinkRequest")


@attr.s(auto_attribs=True)
class RemoteIssueLinkRequest:
    """ Details of a remote issue link. """

    object: None
    global_id: Union[Unset, str] = UNSET
    application: Union[Unset, None] = UNSET
    relationship: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object = None

        global_id = self.global_id
        application = None

        relationship = self.relationship

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object,
            }
        )
        if global_id is not UNSET:
            field_dict["globalId"] = global_id
        if application is not UNSET:
            field_dict["application"] = application
        if relationship is not UNSET:
            field_dict["relationship"] = relationship

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object = None

        global_id = d.pop("globalId", UNSET)

        application = None

        relationship = d.pop("relationship", UNSET)

        remote_issue_link_request = cls(
            object=object,
            global_id=global_id,
            application=application,
            relationship=relationship,
        )

        remote_issue_link_request.additional_properties = d
        return remote_issue_link_request

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
