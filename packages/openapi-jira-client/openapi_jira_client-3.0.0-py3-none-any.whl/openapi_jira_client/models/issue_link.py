from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueLink")


@attr.s(auto_attribs=True)
class IssueLink:
    """ Details of a link between issues. """

    type: None
    inward_issue: None
    outward_issue: None
    id: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = None

        inward_issue = None

        outward_issue = None

        id = self.id
        self_ = self.self_

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
                "inwardIssue": inward_issue,
                "outwardIssue": outward_issue,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = None

        inward_issue = None

        outward_issue = None

        id = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        issue_link = cls(
            type=type,
            inward_issue=inward_issue,
            outward_issue=outward_issue,
            id=id,
            self_=self_,
        )

        return issue_link
