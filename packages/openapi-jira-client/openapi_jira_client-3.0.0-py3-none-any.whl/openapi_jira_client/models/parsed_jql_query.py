from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParsedJqlQuery")


@attr.s(auto_attribs=True)
class ParsedJqlQuery:
    """ Details of a parsed JQL query. """

    query: str
    structure: Union[Unset, None] = UNSET
    errors: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        query = self.query
        structure = None

        errors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "query": query,
            }
        )
        if structure is not UNSET:
            field_dict["structure"] = structure
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query")

        structure = None

        errors = cast(List[str], d.pop("errors", UNSET))

        parsed_jql_query = cls(
            query=query,
            structure=structure,
            errors=errors,
        )

        return parsed_jql_query
