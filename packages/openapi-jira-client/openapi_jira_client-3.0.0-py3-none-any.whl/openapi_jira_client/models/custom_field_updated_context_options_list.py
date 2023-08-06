from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.custom_field_option_update import CustomFieldOptionUpdate
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldUpdatedContextOptionsList")


@attr.s(auto_attribs=True)
class CustomFieldUpdatedContextOptionsList:
    """ A list of custom field options for a context. """

    options: Union[Unset, List[CustomFieldOptionUpdate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        options: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = CustomFieldOptionUpdate.from_dict(options_item_data)

            options.append(options_item)

        custom_field_updated_context_options_list = cls(
            options=options,
        )

        return custom_field_updated_context_options_list
