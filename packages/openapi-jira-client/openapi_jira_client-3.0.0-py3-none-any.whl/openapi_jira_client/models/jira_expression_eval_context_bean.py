from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionEvalContextBean")


@attr.s(auto_attribs=True)
class JiraExpressionEvalContextBean:
    """  """

    issue: Union[Unset, None] = UNSET
    issues: Union[Unset, None] = UNSET
    project: Union[Unset, None] = UNSET
    sprint: Union[Unset, int] = UNSET
    board: Union[Unset, int] = UNSET
    service_desk: Union[Unset, int] = UNSET
    customer_request: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue = None

        issues = None

        project = None

        sprint = self.sprint
        board = self.board
        service_desk = self.service_desk
        customer_request = self.customer_request

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue is not UNSET:
            field_dict["issue"] = issue
        if issues is not UNSET:
            field_dict["issues"] = issues
        if project is not UNSET:
            field_dict["project"] = project
        if sprint is not UNSET:
            field_dict["sprint"] = sprint
        if board is not UNSET:
            field_dict["board"] = board
        if service_desk is not UNSET:
            field_dict["serviceDesk"] = service_desk
        if customer_request is not UNSET:
            field_dict["customerRequest"] = customer_request

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue = None

        issues = None

        project = None

        sprint = d.pop("sprint", UNSET)

        board = d.pop("board", UNSET)

        service_desk = d.pop("serviceDesk", UNSET)

        customer_request = d.pop("customerRequest", UNSET)

        jira_expression_eval_context_bean = cls(
            issue=issue,
            issues=issues,
            project=project,
            sprint=sprint,
            board=board,
            service_desk=service_desk,
            customer_request=customer_request,
        )

        return jira_expression_eval_context_bean
