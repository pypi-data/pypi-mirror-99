from typing import Any, Dict, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionsComplexityBean")


@attr.s(auto_attribs=True)
class JiraExpressionsComplexityBean:
    """  """

    steps: None
    expensive_operations: None
    beans: None
    primitive_values: None

    def to_dict(self) -> Dict[str, Any]:
        steps = None

        expensive_operations = None

        beans = None

        primitive_values = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "steps": steps,
                "expensiveOperations": expensive_operations,
                "beans": beans,
                "primitiveValues": primitive_values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        steps = None

        expensive_operations = None

        beans = None

        primitive_values = None

        jira_expressions_complexity_bean = cls(
            steps=steps,
            expensive_operations=expensive_operations,
            beans=beans,
            primitive_values=primitive_values,
        )

        return jira_expressions_complexity_bean
