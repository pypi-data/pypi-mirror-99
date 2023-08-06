from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.component_with_issue_count_assignee_type import ComponentWithIssueCountAssigneeType
from ..models.component_with_issue_count_real_assignee_type import ComponentWithIssueCountRealAssigneeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentWithIssueCount")


@attr.s(auto_attribs=True)
class ComponentWithIssueCount:
    """ Details about a component with a count of the issues it contains. """

    issue_count: Union[Unset, int] = UNSET
    real_assignee: Union[Unset, None] = UNSET
    real_assignee_type: Union[Unset, ComponentWithIssueCountRealAssigneeType] = UNSET
    is_assignee_type_valid: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    lead: Union[Unset, None] = UNSET
    assignee_type: Union[Unset, ComponentWithIssueCountAssigneeType] = UNSET
    self_: Union[Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    project_id: Union[Unset, int] = UNSET
    assignee: Union[Unset, None] = UNSET
    name: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_count = self.issue_count
        real_assignee = None

        real_assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.real_assignee_type, Unset):
            real_assignee_type = self.real_assignee_type.value

        is_assignee_type_valid = self.is_assignee_type_valid
        description = self.description
        lead = None

        assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.assignee_type, Unset):
            assignee_type = self.assignee_type.value

        self_ = self.self_
        project = self.project
        project_id = self.project_id
        assignee = None

        name = self.name
        id_ = self.id_

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue_count is not UNSET:
            field_dict["issueCount"] = issue_count
        if real_assignee is not UNSET:
            field_dict["realAssignee"] = real_assignee
        if real_assignee_type is not UNSET:
            field_dict["realAssigneeType"] = real_assignee_type
        if is_assignee_type_valid is not UNSET:
            field_dict["isAssigneeTypeValid"] = is_assignee_type_valid
        if description is not UNSET:
            field_dict["description"] = description
        if lead is not UNSET:
            field_dict["lead"] = lead
        if assignee_type is not UNSET:
            field_dict["assigneeType"] = assignee_type
        if self_ is not UNSET:
            field_dict["self"] = self_
        if project is not UNSET:
            field_dict["project"] = project
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if name is not UNSET:
            field_dict["name"] = name
        if id_ is not UNSET:
            field_dict["id"] = id_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_count = d.pop("issueCount", UNSET)

        real_assignee = None

        real_assignee_type: Union[Unset, ComponentWithIssueCountRealAssigneeType] = UNSET
        _real_assignee_type = d.pop("realAssigneeType", UNSET)
        if not isinstance(_real_assignee_type, Unset):
            real_assignee_type = ComponentWithIssueCountRealAssigneeType(_real_assignee_type)

        is_assignee_type_valid = d.pop("isAssigneeTypeValid", UNSET)

        description = d.pop("description", UNSET)

        lead = None

        assignee_type: Union[Unset, ComponentWithIssueCountAssigneeType] = UNSET
        _assignee_type = d.pop("assigneeType", UNSET)
        if not isinstance(_assignee_type, Unset):
            assignee_type = ComponentWithIssueCountAssigneeType(_assignee_type)

        self_ = d.pop("self", UNSET)

        project = d.pop("project", UNSET)

        project_id = d.pop("projectId", UNSET)

        assignee = None

        name = d.pop("name", UNSET)

        id_ = d.pop("id", UNSET)

        component_with_issue_count = cls(
            issue_count=issue_count,
            real_assignee=real_assignee,
            real_assignee_type=real_assignee_type,
            is_assignee_type_valid=is_assignee_type_valid,
            description=description,
            lead=lead,
            assignee_type=assignee_type,
            self_=self_,
            project=project,
            project_id=project_id,
            assignee=assignee,
            name=name,
            id_=id_,
        )

        return component_with_issue_count
