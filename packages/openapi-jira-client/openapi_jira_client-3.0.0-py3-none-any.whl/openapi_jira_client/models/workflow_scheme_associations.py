from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowSchemeAssociations")


@attr.s(auto_attribs=True)
class WorkflowSchemeAssociations:
    """ A workflow scheme along with a list of projects that use it. """

    project_ids: List[str]
    workflow_scheme: None

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self.project_ids

        workflow_scheme = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectIds": project_ids,
                "workflowScheme": workflow_scheme,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_ids = cast(List[str], d.pop("projectIds"))

        workflow_scheme = None

        workflow_scheme_associations = cls(
            project_ids=project_ids,
            workflow_scheme=workflow_scheme,
        )

        return workflow_scheme_associations
