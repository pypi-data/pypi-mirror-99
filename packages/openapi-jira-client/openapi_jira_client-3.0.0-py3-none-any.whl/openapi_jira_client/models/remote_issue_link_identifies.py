from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteIssueLinkIdentifies")


@attr.s(auto_attribs=True)
class RemoteIssueLinkIdentifies:
    """ Details of the identifiers for a created or updated remote issue link. """

    id: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        self_ = self.self_

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        remote_issue_link_identifies = cls(
            id=id,
            self_=self_,
        )

        return remote_issue_link_identifies
