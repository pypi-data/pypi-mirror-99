from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionEvaluationMetaDataBean")


@attr.s(auto_attribs=True)
class JiraExpressionEvaluationMetaDataBean:
    """  """

    complexity: Union[Unset, None] = UNSET
    issues: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        complexity = None

        issues = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if complexity is not UNSET:
            field_dict["complexity"] = complexity
        if issues is not UNSET:
            field_dict["issues"] = issues

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        complexity = None

        issues = None

        jira_expression_evaluation_meta_data_bean = cls(
            complexity=complexity,
            issues=issues,
        )

        return jira_expression_evaluation_meta_data_bean
