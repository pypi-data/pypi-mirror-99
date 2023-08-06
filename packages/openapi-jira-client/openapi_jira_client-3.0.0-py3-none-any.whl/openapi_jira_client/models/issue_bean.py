from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.included_fields import IncludedFields
from ..models.issue_bean_fields import IssueBeanFields
from ..models.issue_bean_names import IssueBeanNames
from ..models.issue_bean_properties import IssueBeanProperties
from ..models.issue_bean_rendered_fields import IssueBeanRenderedFields
from ..models.issue_bean_schema import IssueBeanSchema
from ..models.issue_bean_versioned_representations import IssueBeanVersionedRepresentations
from ..models.issue_transition import IssueTransition
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueBean")


@attr.s(auto_attribs=True)
class IssueBean:
    """  """

    expand: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    rendered_fields: Union[IssueBeanRenderedFields, Unset] = UNSET
    properties: Union[IssueBeanProperties, Unset] = UNSET
    names: Union[IssueBeanNames, Unset] = UNSET
    schema: Union[IssueBeanSchema, Unset] = UNSET
    transitions: Union[Unset, List[IssueTransition]] = UNSET
    operations: Union[Unset, None] = UNSET
    editmeta: Union[Unset, None] = UNSET
    changelog: Union[Unset, None] = UNSET
    versioned_representations: Union[IssueBeanVersionedRepresentations, Unset] = UNSET
    fields_to_include: Union[IncludedFields, Unset] = UNSET
    fields: Union[IssueBeanFields, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        id = self.id
        self_ = self.self_
        key = self.key
        rendered_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rendered_fields, Unset):
            rendered_fields = self.rendered_fields.to_dict()

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        names: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.names, Unset):
            names = self.names.to_dict()

        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        transitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.transitions, Unset):
            transitions = []
            for transitions_item_data in self.transitions:
                transitions_item = transitions_item_data.to_dict()

                transitions.append(transitions_item)

        operations = None

        editmeta = None

        changelog = None

        versioned_representations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.versioned_representations, Unset):
            versioned_representations = self.versioned_representations.to_dict()

        fields_to_include: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields_to_include, Unset):
            fields_to_include = self.fields_to_include.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if id is not UNSET:
            field_dict["id"] = id
        if self_ is not UNSET:
            field_dict["self"] = self_
        if key is not UNSET:
            field_dict["key"] = key
        if rendered_fields is not UNSET:
            field_dict["renderedFields"] = rendered_fields
        if properties is not UNSET:
            field_dict["properties"] = properties
        if names is not UNSET:
            field_dict["names"] = names
        if schema is not UNSET:
            field_dict["schema"] = schema
        if transitions is not UNSET:
            field_dict["transitions"] = transitions
        if operations is not UNSET:
            field_dict["operations"] = operations
        if editmeta is not UNSET:
            field_dict["editmeta"] = editmeta
        if changelog is not UNSET:
            field_dict["changelog"] = changelog
        if versioned_representations is not UNSET:
            field_dict["versionedRepresentations"] = versioned_representations
        if fields_to_include is not UNSET:
            field_dict["fieldsToInclude"] = fields_to_include
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        id = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        key = d.pop("key", UNSET)

        rendered_fields: Union[IssueBeanRenderedFields, Unset] = UNSET
        _rendered_fields = d.pop("renderedFields", UNSET)
        if not isinstance(_rendered_fields, Unset):
            rendered_fields = IssueBeanRenderedFields.from_dict(_rendered_fields)

        properties: Union[IssueBeanProperties, Unset] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = IssueBeanProperties.from_dict(_properties)

        names: Union[IssueBeanNames, Unset] = UNSET
        _names = d.pop("names", UNSET)
        if not isinstance(_names, Unset):
            names = IssueBeanNames.from_dict(_names)

        schema: Union[IssueBeanSchema, Unset] = UNSET
        _schema = d.pop("schema", UNSET)
        if not isinstance(_schema, Unset):
            schema = IssueBeanSchema.from_dict(_schema)

        transitions = []
        _transitions = d.pop("transitions", UNSET)
        for transitions_item_data in _transitions or []:
            transitions_item = IssueTransition.from_dict(transitions_item_data)

            transitions.append(transitions_item)

        operations = None

        editmeta = None

        changelog = None

        versioned_representations: Union[IssueBeanVersionedRepresentations, Unset] = UNSET
        _versioned_representations = d.pop("versionedRepresentations", UNSET)
        if not isinstance(_versioned_representations, Unset):
            versioned_representations = IssueBeanVersionedRepresentations.from_dict(_versioned_representations)

        fields_to_include: Union[IncludedFields, Unset] = UNSET
        _fields_to_include = d.pop("fieldsToInclude", UNSET)
        if not isinstance(_fields_to_include, Unset):
            fields_to_include = IncludedFields.from_dict(_fields_to_include)

        fields: Union[IssueBeanFields, Unset] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = IssueBeanFields.from_dict(_fields)

        issue_bean = cls(
            expand=expand,
            id=id,
            self_=self_,
            key=key,
            rendered_fields=rendered_fields,
            properties=properties,
            names=names,
            schema=schema,
            transitions=transitions,
            operations=operations,
            editmeta=editmeta,
            changelog=changelog,
            versioned_representations=versioned_representations,
            fields_to_include=fields_to_include,
            fields=fields,
        )

        return issue_bean
