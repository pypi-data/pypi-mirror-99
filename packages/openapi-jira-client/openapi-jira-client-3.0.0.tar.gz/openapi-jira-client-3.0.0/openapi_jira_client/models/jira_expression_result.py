from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionResult")


@attr.s(auto_attribs=True)
class JiraExpressionResult:
    """ The result of evaluating a Jira expression. """

    value: None
    meta: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = None

        meta = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
            }
        )
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = None

        meta = None

        jira_expression_result = cls(
            value=value,
            meta=meta,
        )

        return jira_expression_result
