from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteObject")


@attr.s(auto_attribs=True)
class RemoteObject:
    """ The linked item. """

    url: str
    title: str
    summary: Union[Unset, str] = UNSET
    icon: Union[Unset, None] = UNSET
    status: Union[Unset, None] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        title = self.title
        summary = self.summary
        icon = None

        status = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "title": title,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if icon is not UNSET:
            field_dict["icon"] = icon
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        title = d.pop("title")

        summary = d.pop("summary", UNSET)

        icon = None

        status = None

        remote_object = cls(
            url=url,
            title=title,
            summary=summary,
            icon=icon,
            status=status,
        )

        remote_object.additional_properties = d
        return remote_object

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
