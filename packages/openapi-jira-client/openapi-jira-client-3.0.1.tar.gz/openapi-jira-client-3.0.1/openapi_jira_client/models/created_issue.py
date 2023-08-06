from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatedIssue")


@attr.s(auto_attribs=True)
class CreatedIssue:
    """ Details about a created issue or subtask. """

    id_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    transition: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        key = self.key
        self_ = self.self_
        transition = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if key is not UNSET:
            field_dict["key"] = key
        if self_ is not UNSET:
            field_dict["self"] = self_
        if transition is not UNSET:
            field_dict["transition"] = transition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        self_ = d.pop("self", UNSET)

        transition = None

        created_issue = cls(
            id_=id_,
            key=key,
            self_=self_,
            transition=transition,
        )

        return created_issue
