from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.screen_id import ScreenID
from ..models.transition_type import TransitionType
from ..models.workflow_rules import WorkflowRules
from ..types import UNSET, Unset

T = TypeVar("T", bound="Transition")


@attr.s(auto_attribs=True)
class Transition:
    """ Details of a workflow transition. """

    id: str
    name: str
    description: str
    from_: List[str]
    to: str
    type: TransitionType
    screen: Union[ScreenID, Unset] = UNSET
    rules: Union[WorkflowRules, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        description = self.description
        from_ = self.from_

        to = self.to
        type = self.type.value

        screen: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.screen, Unset):
            screen = self.screen.to_dict()

        rules: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = self.rules.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "from": from_,
                "to": to,
                "type": type,
            }
        )
        if screen is not UNSET:
            field_dict["screen"] = screen
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        from_ = cast(List[str], d.pop("from"))

        to = d.pop("to")

        type = TransitionType(d.pop("type"))

        screen: Union[ScreenID, Unset] = UNSET
        _screen = d.pop("screen", UNSET)
        if not isinstance(_screen, Unset):
            screen = ScreenID.from_dict(_screen)

        rules: Union[WorkflowRules, Unset] = UNSET
        _rules = d.pop("rules", UNSET)
        if not isinstance(_rules, Unset):
            rules = WorkflowRules.from_dict(_rules)

        transition = cls(
            id=id,
            name=name,
            description=description,
            from_=from_,
            to=to,
            type=type,
            screen=screen,
            rules=rules,
        )

        return transition
