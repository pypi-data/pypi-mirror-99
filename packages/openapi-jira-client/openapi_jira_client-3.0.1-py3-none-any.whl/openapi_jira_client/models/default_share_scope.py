from typing import Any, Dict, Type, TypeVar

import attr

from ..models.default_share_scope_scope import DefaultShareScopeScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="DefaultShareScope")


@attr.s(auto_attribs=True)
class DefaultShareScope:
    """ Details of the scope of the default sharing for new filters and dashboards. """

    scope: DefaultShareScopeScope

    def to_dict(self) -> Dict[str, Any]:
        scope = self.scope.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "scope": scope,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        scope = DefaultShareScopeScope(d.pop("scope"))

        default_share_scope = cls(
            scope=scope,
        )

        return default_share_scope
