import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.entity_property import EntityProperty
from ..types import UNSET, Unset

T = TypeVar("T", bound="Comment")


@attr.s(auto_attribs=True)
class Comment:
    """ A comment. """

    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    author: Union[Unset, None] = UNSET
    body: Union[Unset, None] = UNSET
    rendered_body: Union[Unset, str] = UNSET
    update_author: Union[Unset, None] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    visibility: Union[Unset, None] = UNSET
    jsd_public: Union[Unset, bool] = UNSET
    properties: Union[Unset, List[EntityProperty]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        author = None

        body = None

        rendered_body = self.rendered_body
        update_author = None

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        visibility = None

        jsd_public = self.jsd_public
        properties: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = []
            for properties_item_data in self.properties:
                properties_item = properties_item_data.to_dict()

                properties.append(properties_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if author is not UNSET:
            field_dict["author"] = author
        if body is not UNSET:
            field_dict["body"] = body
        if rendered_body is not UNSET:
            field_dict["renderedBody"] = rendered_body
        if update_author is not UNSET:
            field_dict["updateAuthor"] = update_author
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if jsd_public is not UNSET:
            field_dict["jsdPublic"] = jsd_public
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        author = None

        body = None

        rendered_body = d.pop("renderedBody", UNSET)

        update_author = None

        created: Union[Unset, datetime.datetime] = UNSET
        _created = d.pop("created", UNSET)
        if not isinstance(_created, Unset):
            created = isoparse(_created)

        updated: Union[Unset, datetime.datetime] = UNSET
        _updated = d.pop("updated", UNSET)
        if not isinstance(_updated, Unset):
            updated = isoparse(_updated)

        visibility = None

        jsd_public = d.pop("jsdPublic", UNSET)

        properties = []
        _properties = d.pop("properties", UNSET)
        for properties_item_data in _properties or []:
            properties_item = EntityProperty.from_dict(properties_item_data)

            properties.append(properties_item)

        comment = cls(
            self_=self_,
            id_=id_,
            author=author,
            body=body,
            rendered_body=rendered_body,
            update_author=update_author,
            created=created,
            updated=updated,
            visibility=visibility,
            jsd_public=jsd_public,
            properties=properties,
        )

        comment.additional_properties = d
        return comment

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
