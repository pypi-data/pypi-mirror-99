from typing import Any, Dict, Type, TypeVar

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTransition")


@attr.s(auto_attribs=True)
class WorkflowTransition:
    """ A workflow transition. """

    id: int
    name: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        workflow_transition = cls(
            id=id,
            name=name,
        )

        return workflow_transition
