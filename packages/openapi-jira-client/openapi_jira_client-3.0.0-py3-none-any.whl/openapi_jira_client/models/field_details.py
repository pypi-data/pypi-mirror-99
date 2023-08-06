from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldDetails")


@attr.s(auto_attribs=True)
class FieldDetails:
    """ Details about a field. """

    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    custom: Union[Unset, bool] = UNSET
    orderable: Union[Unset, bool] = UNSET
    navigable: Union[Unset, bool] = UNSET
    searchable: Union[Unset, bool] = UNSET
    clause_names: Union[Unset, List[str]] = UNSET
    scope: Union[Unset, None] = UNSET
    schema: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        key = self.key
        name = self.name
        custom = self.custom
        orderable = self.orderable
        navigable = self.navigable
        searchable = self.searchable
        clause_names: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.clause_names, Unset):
            clause_names = self.clause_names

        scope = None

        schema = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if custom is not UNSET:
            field_dict["custom"] = custom
        if orderable is not UNSET:
            field_dict["orderable"] = orderable
        if navigable is not UNSET:
            field_dict["navigable"] = navigable
        if searchable is not UNSET:
            field_dict["searchable"] = searchable
        if clause_names is not UNSET:
            field_dict["clauseNames"] = clause_names
        if scope is not UNSET:
            field_dict["scope"] = scope
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        custom = d.pop("custom", UNSET)

        orderable = d.pop("orderable", UNSET)

        navigable = d.pop("navigable", UNSET)

        searchable = d.pop("searchable", UNSET)

        clause_names = cast(List[str], d.pop("clauseNames", UNSET))

        scope = None

        schema = None

        field_details = cls(
            id=id,
            key=key,
            name=name,
            custom=custom,
            orderable=orderable,
            navigable=navigable,
            searchable=searchable,
            clause_names=clause_names,
            scope=scope,
            schema=schema,
        )

        return field_details
