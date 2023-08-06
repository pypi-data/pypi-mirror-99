from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.rule_configuration import RuleConfiguration
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectWorkflowTransitionRule")


@attr.s(auto_attribs=True)
class ConnectWorkflowTransitionRule:
    """ A workflow transition rule. """

    id_: str
    key: str
    configuration: RuleConfiguration
    transition: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        key = self.key
        configuration = self.configuration.to_dict()

        transition = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "key": key,
                "configuration": configuration,
            }
        )
        if transition is not UNSET:
            field_dict["transition"] = transition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        key = d.pop("key")

        configuration = RuleConfiguration.from_dict(d.pop("configuration"))

        transition = None

        connect_workflow_transition_rule = cls(
            id_=id_,
            key=key,
            configuration=configuration,
            transition=transition,
        )

        return connect_workflow_transition_rule
