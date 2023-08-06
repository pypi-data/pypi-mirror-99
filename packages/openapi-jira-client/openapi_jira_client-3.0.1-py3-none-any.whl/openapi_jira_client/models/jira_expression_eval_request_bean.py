from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionEvalRequestBean")


@attr.s(auto_attribs=True)
class JiraExpressionEvalRequestBean:
    """  """

    expression: str
    context: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expression = self.expression
        context = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expression": expression,
            }
        )
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expression = d.pop("expression")

        context = None

        jira_expression_eval_request_bean = cls(
            expression=expression,
            context=context,
        )

        return jira_expression_eval_request_bean
