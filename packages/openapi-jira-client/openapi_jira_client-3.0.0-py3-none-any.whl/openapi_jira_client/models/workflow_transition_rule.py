from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTransitionRule")


@attr.s(auto_attribs=True)
class WorkflowTransitionRule:
    """ A workflow transition rule. """

    type: str
    configuration: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        configuration = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
            }
        )
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        configuration = None

        workflow_transition_rule = cls(
            type=type,
            configuration=configuration,
        )

        return workflow_transition_rule
