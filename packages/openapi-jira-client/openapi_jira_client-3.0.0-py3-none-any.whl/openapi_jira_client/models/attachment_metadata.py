import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.attachment_metadata_properties import AttachmentMetadataProperties
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentMetadata")


@attr.s(auto_attribs=True)
class AttachmentMetadata:
    """ Metadata for an issue attachment. """

    id: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    author: Union[Unset, None] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    size: Union[Unset, int] = UNSET
    mime_type: Union[Unset, str] = UNSET
    properties: Union[AttachmentMetadataProperties, Unset] = UNSET
    content: Union[Unset, str] = UNSET
    thumbnail: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        self_ = self.self_
        filename = self.filename
        author = None

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        size = self.size
        mime_type = self.mime_type
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        content = self.content
        thumbnail = self.thumbnail

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if self_ is not UNSET:
            field_dict["self"] = self_
        if filename is not UNSET:
            field_dict["filename"] = filename
        if author is not UNSET:
            field_dict["author"] = author
        if created is not UNSET:
            field_dict["created"] = created
        if size is not UNSET:
            field_dict["size"] = size
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if properties is not UNSET:
            field_dict["properties"] = properties
        if content is not UNSET:
            field_dict["content"] = content
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        filename = d.pop("filename", UNSET)

        author = None

        created: Union[Unset, datetime.datetime] = UNSET
        _created = d.pop("created", UNSET)
        if not isinstance(_created, Unset):
            created = isoparse(_created)

        size = d.pop("size", UNSET)

        mime_type = d.pop("mimeType", UNSET)

        properties: Union[AttachmentMetadataProperties, Unset] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = AttachmentMetadataProperties.from_dict(_properties)

        content = d.pop("content", UNSET)

        thumbnail = d.pop("thumbnail", UNSET)

        attachment_metadata = cls(
            id=id,
            self_=self_,
            filename=filename,
            author=author,
            created=created,
            size=size,
            mime_type=mime_type,
            properties=properties,
            content=content,
            thumbnail=thumbnail,
        )

        return attachment_metadata
