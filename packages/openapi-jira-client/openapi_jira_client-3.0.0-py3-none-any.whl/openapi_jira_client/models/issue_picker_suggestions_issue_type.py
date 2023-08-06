from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.suggested_issue import SuggestedIssue
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssuePickerSuggestionsIssueType")


@attr.s(auto_attribs=True)
class IssuePickerSuggestionsIssueType:
    """ A type of issue suggested for use in auto-completion. """

    label: Union[Unset, str] = UNSET
    sub: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    msg: Union[Unset, str] = UNSET
    issues: Union[Unset, List[SuggestedIssue]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        sub = self.sub
        id = self.id
        msg = self.msg
        issues: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = []
            for issues_item_data in self.issues:
                issues_item = issues_item_data.to_dict()

                issues.append(issues_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if sub is not UNSET:
            field_dict["sub"] = sub
        if id is not UNSET:
            field_dict["id"] = id
        if msg is not UNSET:
            field_dict["msg"] = msg
        if issues is not UNSET:
            field_dict["issues"] = issues

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        sub = d.pop("sub", UNSET)

        id = d.pop("id", UNSET)

        msg = d.pop("msg", UNSET)

        issues = []
        _issues = d.pop("issues", UNSET)
        for issues_item_data in _issues or []:
            issues_item = SuggestedIssue.from_dict(issues_item_data)

            issues.append(issues_item)

        issue_picker_suggestions_issue_type = cls(
            label=label,
            sub=sub,
            id=id,
            msg=msg,
            issues=issues,
        )

        return issue_picker_suggestions_issue_type
