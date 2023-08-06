from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteIssueLink")


@attr.s(auto_attribs=True)
class RemoteIssueLink:
    """ Details of an issue remote link. """

    id: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    global_id: Union[Unset, str] = UNSET
    application: Union[Unset, None] = UNSET
    relationship: Union[Unset, str] = UNSET
    object: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        self_ = self.self_
        global_id = self.global_id
        application = None

        relationship = self.relationship
        object = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if self_ is not UNSET:
            field_dict["self"] = self_
        if global_id is not UNSET:
            field_dict["globalId"] = global_id
        if application is not UNSET:
            field_dict["application"] = application
        if relationship is not UNSET:
            field_dict["relationship"] = relationship
        if object is not UNSET:
            field_dict["object"] = object

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        global_id = d.pop("globalId", UNSET)

        application = None

        relationship = d.pop("relationship", UNSET)

        object = None

        remote_issue_link = cls(
            id=id,
            self_=self_,
            global_id=global_id,
            application=application,
            relationship=relationship,
            object=object,
        )

        return remote_issue_link
