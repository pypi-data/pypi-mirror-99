from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.issue_type_details import IssueTypeDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="Fields")


@attr.s(auto_attribs=True)
class Fields:
    """ Key fields from the linked issue. """

    summary: Union[Unset, str] = UNSET
    status: Union[Unset, None] = UNSET
    priority: Union[Unset, None] = UNSET
    assignee: Union[Unset, None] = UNSET
    timetracking: Union[Unset, None] = UNSET
    issuetype: Union[Unset, IssueTypeDetails] = UNSET
    issue_type: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        status = None

        priority = None

        assignee = None

        timetracking = None

        issuetype: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issuetype, Unset):
            issuetype = self.issuetype.to_dict()

        issue_type = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if summary is not UNSET:
            field_dict["summary"] = summary
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if timetracking is not UNSET:
            field_dict["timetracking"] = timetracking
        if issuetype is not UNSET:
            field_dict["issuetype"] = issuetype
        if issue_type is not UNSET:
            field_dict["issueType"] = issue_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        summary = d.pop("summary", UNSET)

        status = None

        priority = None

        assignee = None

        timetracking = None

        issuetype: Union[Unset, IssueTypeDetails] = UNSET
        _issuetype = d.pop("issuetype", UNSET)
        if not isinstance(_issuetype, Unset):
            issuetype = IssueTypeDetails.from_dict(_issuetype)

        issue_type = None

        fields = cls(
            summary=summary,
            status=status,
            priority=priority,
            assignee=assignee,
            timetracking=timetracking,
            issuetype=issuetype,
            issue_type=issue_type,
        )

        return fields
