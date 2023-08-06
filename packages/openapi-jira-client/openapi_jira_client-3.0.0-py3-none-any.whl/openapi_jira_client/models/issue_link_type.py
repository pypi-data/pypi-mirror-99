from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueLinkType")


@attr.s(auto_attribs=True)
class IssueLinkType:
    """This object is used as follows:

    *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it defines and reports on the type of link between the issues. Find a list of issue link types with [Get issue link types](#api-rest-api-3-issueLinkType-get).
    *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it defines and reports on issue link types."""

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    inward: Union[Unset, str] = UNSET
    outward: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        inward = self.inward
        outward = self.outward
        self_ = self.self_

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if inward is not UNSET:
            field_dict["inward"] = inward
        if outward is not UNSET:
            field_dict["outward"] = outward
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        inward = d.pop("inward", UNSET)

        outward = d.pop("outward", UNSET)

        self_ = d.pop("self", UNSET)

        issue_link_type = cls(
            id=id,
            name=name,
            inward=inward,
            outward=outward,
            self_=self_,
        )

        return issue_link_type
