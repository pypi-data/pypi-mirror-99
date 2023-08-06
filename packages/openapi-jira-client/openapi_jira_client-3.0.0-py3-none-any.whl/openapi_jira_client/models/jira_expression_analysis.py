from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.jira_expression_complexity import JiraExpressionComplexity
from ..models.jira_expression_validation_error import JiraExpressionValidationError
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionAnalysis")


@attr.s(auto_attribs=True)
class JiraExpressionAnalysis:
    """ Details about the analysed Jira expression. """

    expression: str
    valid: bool
    errors: Union[Unset, List[JiraExpressionValidationError]] = UNSET
    type: Union[Unset, str] = UNSET
    complexity: Union[JiraExpressionComplexity, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expression = self.expression
        valid = self.valid
        errors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()

                errors.append(errors_item)

        type = self.type
        complexity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.complexity, Unset):
            complexity = self.complexity.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expression": expression,
                "valid": valid,
            }
        )
        if errors is not UNSET:
            field_dict["errors"] = errors
        if type is not UNSET:
            field_dict["type"] = type
        if complexity is not UNSET:
            field_dict["complexity"] = complexity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expression = d.pop("expression")

        valid = d.pop("valid")

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = JiraExpressionValidationError.from_dict(errors_item_data)

            errors.append(errors_item)

        type = d.pop("type", UNSET)

        complexity: Union[JiraExpressionComplexity, Unset] = UNSET
        _complexity = d.pop("complexity", UNSET)
        if not isinstance(_complexity, Unset):
            complexity = JiraExpressionComplexity.from_dict(_complexity)

        jira_expression_analysis = cls(
            expression=expression,
            valid=valid,
            errors=errors,
            type=type,
            complexity=complexity,
        )

        return jira_expression_analysis
