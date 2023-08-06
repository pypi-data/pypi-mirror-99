from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.project_scope_bean import ProjectScopeBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueFieldOptionScopeBean")


@attr.s(auto_attribs=True)
class IssueFieldOptionScopeBean:
    """  """

    projects: Union[Unset, List[int]] = UNSET
    projects2: Union[Unset, List[ProjectScopeBean]] = UNSET
    global_: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        projects: Union[Unset, List[int]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = self.projects

        projects2: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.projects2, Unset):
            projects2 = []
            for projects2_item_data in self.projects2:
                projects2_item = projects2_item_data.to_dict()

                projects2.append(projects2_item)

        global_ = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if projects is not UNSET:
            field_dict["projects"] = projects
        if projects2 is not UNSET:
            field_dict["projects2"] = projects2
        if global_ is not UNSET:
            field_dict["global"] = global_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        projects = cast(List[int], d.pop("projects", UNSET))

        projects2 = []
        _projects2 = d.pop("projects2", UNSET)
        for projects2_item_data in _projects2 or []:
            projects2_item = ProjectScopeBean.from_dict(projects2_item_data)

            projects2.append(projects2_item)

        global_ = None

        issue_field_option_scope_bean = cls(
            projects=projects,
            projects2=projects2,
            global_=global_,
        )

        return issue_field_option_scope_bean
