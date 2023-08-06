from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.field_reference_data_auto import FieldReferenceDataAuto
from ..models.field_reference_data_orderable import FieldReferenceDataOrderable
from ..models.field_reference_data_searchable import FieldReferenceDataSearchable
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldReferenceData")


@attr.s(auto_attribs=True)
class FieldReferenceData:
    """ Details of a field that can be used in advanced searches. """

    value: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    orderable: Union[Unset, FieldReferenceDataOrderable] = UNSET
    searchable: Union[Unset, FieldReferenceDataSearchable] = UNSET
    auto: Union[Unset, FieldReferenceDataAuto] = UNSET
    cfid: Union[Unset, str] = UNSET
    operators: Union[Unset, List[str]] = UNSET
    types: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        display_name = self.display_name
        orderable: Union[Unset, FieldReferenceDataOrderable] = UNSET
        if not isinstance(self.orderable, Unset):
            orderable = self.orderable

        searchable: Union[Unset, FieldReferenceDataSearchable] = UNSET
        if not isinstance(self.searchable, Unset):
            searchable = self.searchable

        auto: Union[Unset, FieldReferenceDataAuto] = UNSET
        if not isinstance(self.auto, Unset):
            auto = self.auto

        cfid = self.cfid
        operators: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.operators, Unset):
            operators = self.operators

        types: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.types, Unset):
            types = self.types

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if orderable is not UNSET:
            field_dict["orderable"] = orderable
        if searchable is not UNSET:
            field_dict["searchable"] = searchable
        if auto is not UNSET:
            field_dict["auto"] = auto
        if cfid is not UNSET:
            field_dict["cfid"] = cfid
        if operators is not UNSET:
            field_dict["operators"] = operators
        if types is not UNSET:
            field_dict["types"] = types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        display_name = d.pop("displayName", UNSET)

        orderable: Union[Unset, FieldReferenceDataOrderable] = UNSET
        _orderable = d.pop("orderable", UNSET)
        if not isinstance(_orderable, Unset):
            orderable = FieldReferenceDataOrderable(_orderable)

        searchable: Union[Unset, FieldReferenceDataSearchable] = UNSET
        _searchable = d.pop("searchable", UNSET)
        if not isinstance(_searchable, Unset):
            searchable = FieldReferenceDataSearchable(_searchable)

        auto: Union[Unset, FieldReferenceDataAuto] = UNSET
        _auto = d.pop("auto", UNSET)
        if not isinstance(_auto, Unset):
            auto = FieldReferenceDataAuto(_auto)

        cfid = d.pop("cfid", UNSET)

        operators = cast(List[str], d.pop("operators", UNSET))

        types = cast(List[str], d.pop("types", UNSET))

        field_reference_data = cls(
            value=value,
            display_name=display_name,
            orderable=orderable,
            searchable=searchable,
            auto=auto,
            cfid=cfid,
            operators=operators,
            types=types,
        )

        return field_reference_data
