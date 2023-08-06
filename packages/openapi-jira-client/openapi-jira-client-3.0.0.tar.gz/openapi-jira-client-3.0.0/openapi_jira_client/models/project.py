import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.component import Component
from ..models.issue_type_details import IssueTypeDetails
from ..models.project_assignee_type import ProjectAssigneeType
from ..models.project_project_type_key import ProjectProjectTypeKey
from ..models.project_properties import ProjectProperties
from ..models.project_roles import ProjectRoles
from ..models.project_style import ProjectStyle
from ..models.version import Version
from ..types import UNSET, Unset

T = TypeVar("T", bound="Project")


@attr.s(auto_attribs=True)
class Project:
    """ Details about a project. """

    expand: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    lead: Union[Unset, None] = UNSET
    components: Union[Unset, List[Component]] = UNSET
    issue_types: Union[Unset, List[IssueTypeDetails]] = UNSET
    url: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    assignee_type: Union[Unset, ProjectAssigneeType] = UNSET
    versions: Union[Unset, List[Version]] = UNSET
    name: Union[Unset, str] = UNSET
    roles: Union[ProjectRoles, Unset] = UNSET
    avatar_urls: Union[Unset, None] = UNSET
    project_category: Union[Unset, None] = UNSET
    project_type_key: Union[Unset, ProjectProjectTypeKey] = UNSET
    simplified: Union[Unset, bool] = UNSET
    style: Union[Unset, ProjectStyle] = UNSET
    favourite: Union[Unset, bool] = UNSET
    is_private: Union[Unset, bool] = UNSET
    issue_type_hierarchy: Union[Unset, None] = UNSET
    permissions: Union[Unset, None] = UNSET
    properties: Union[ProjectProperties, Unset] = UNSET
    uuid: Union[Unset, str] = UNSET
    insight: Union[Unset, None] = UNSET
    deleted: Union[Unset, bool] = UNSET
    retention_till_date: Union[Unset, datetime.datetime] = UNSET
    deleted_date: Union[Unset, datetime.datetime] = UNSET
    deleted_by: Union[Unset, None] = UNSET
    archived: Union[Unset, bool] = UNSET
    archived_date: Union[Unset, datetime.datetime] = UNSET
    archived_by: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        self_ = self.self_
        id = self.id
        key = self.key
        description = self.description
        lead = None

        components: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()

                components.append(components_item)

        issue_types: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.issue_types, Unset):
            issue_types = []
            for issue_types_item_data in self.issue_types:
                issue_types_item = issue_types_item_data.to_dict()

                issue_types.append(issue_types_item)

        url = self.url
        email = self.email
        assignee_type: Union[Unset, ProjectAssigneeType] = UNSET
        if not isinstance(self.assignee_type, Unset):
            assignee_type = self.assignee_type

        versions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                versions_item = versions_item_data.to_dict()

                versions.append(versions_item)

        name = self.name
        roles: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles.to_dict()

        avatar_urls = None

        project_category = None

        project_type_key: Union[Unset, ProjectProjectTypeKey] = UNSET
        if not isinstance(self.project_type_key, Unset):
            project_type_key = self.project_type_key

        simplified = self.simplified
        style: Union[Unset, ProjectStyle] = UNSET
        if not isinstance(self.style, Unset):
            style = self.style

        favourite = self.favourite
        is_private = self.is_private
        issue_type_hierarchy = None

        permissions = None

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        uuid = self.uuid
        insight = None

        deleted = self.deleted
        retention_till_date: Union[Unset, str] = UNSET
        if not isinstance(self.retention_till_date, Unset):
            retention_till_date = self.retention_till_date.isoformat()

        deleted_date: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_date, Unset):
            deleted_date = self.deleted_date.isoformat()

        deleted_by = None

        archived = self.archived
        archived_date: Union[Unset, str] = UNSET
        if not isinstance(self.archived_date, Unset):
            archived_date = self.archived_date.isoformat()

        archived_by = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if description is not UNSET:
            field_dict["description"] = description
        if lead is not UNSET:
            field_dict["lead"] = lead
        if components is not UNSET:
            field_dict["components"] = components
        if issue_types is not UNSET:
            field_dict["issueTypes"] = issue_types
        if url is not UNSET:
            field_dict["url"] = url
        if email is not UNSET:
            field_dict["email"] = email
        if assignee_type is not UNSET:
            field_dict["assigneeType"] = assignee_type
        if versions is not UNSET:
            field_dict["versions"] = versions
        if name is not UNSET:
            field_dict["name"] = name
        if roles is not UNSET:
            field_dict["roles"] = roles
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if project_category is not UNSET:
            field_dict["projectCategory"] = project_category
        if project_type_key is not UNSET:
            field_dict["projectTypeKey"] = project_type_key
        if simplified is not UNSET:
            field_dict["simplified"] = simplified
        if style is not UNSET:
            field_dict["style"] = style
        if favourite is not UNSET:
            field_dict["favourite"] = favourite
        if is_private is not UNSET:
            field_dict["isPrivate"] = is_private
        if issue_type_hierarchy is not UNSET:
            field_dict["issueTypeHierarchy"] = issue_type_hierarchy
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if properties is not UNSET:
            field_dict["properties"] = properties
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if insight is not UNSET:
            field_dict["insight"] = insight
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if retention_till_date is not UNSET:
            field_dict["retentionTillDate"] = retention_till_date
        if deleted_date is not UNSET:
            field_dict["deletedDate"] = deleted_date
        if deleted_by is not UNSET:
            field_dict["deletedBy"] = deleted_by
        if archived is not UNSET:
            field_dict["archived"] = archived
        if archived_date is not UNSET:
            field_dict["archivedDate"] = archived_date
        if archived_by is not UNSET:
            field_dict["archivedBy"] = archived_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        self_ = d.pop("self", UNSET)

        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        description = d.pop("description", UNSET)

        lead = None

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = Component.from_dict(components_item_data)

            components.append(components_item)

        issue_types = []
        _issue_types = d.pop("issueTypes", UNSET)
        for issue_types_item_data in _issue_types or []:
            issue_types_item = IssueTypeDetails.from_dict(issue_types_item_data)

            issue_types.append(issue_types_item)

        url = d.pop("url", UNSET)

        email = d.pop("email", UNSET)

        assignee_type: Union[Unset, ProjectAssigneeType] = UNSET
        _assignee_type = d.pop("assigneeType", UNSET)
        if not isinstance(_assignee_type, Unset):
            assignee_type = ProjectAssigneeType(_assignee_type)

        versions = []
        _versions = d.pop("versions", UNSET)
        for versions_item_data in _versions or []:
            versions_item = Version.from_dict(versions_item_data)

            versions.append(versions_item)

        name = d.pop("name", UNSET)

        roles: Union[ProjectRoles, Unset] = UNSET
        _roles = d.pop("roles", UNSET)
        if not isinstance(_roles, Unset):
            roles = ProjectRoles.from_dict(_roles)

        avatar_urls = None

        project_category = None

        project_type_key: Union[Unset, ProjectProjectTypeKey] = UNSET
        _project_type_key = d.pop("projectTypeKey", UNSET)
        if not isinstance(_project_type_key, Unset):
            project_type_key = ProjectProjectTypeKey(_project_type_key)

        simplified = d.pop("simplified", UNSET)

        style: Union[Unset, ProjectStyle] = UNSET
        _style = d.pop("style", UNSET)
        if not isinstance(_style, Unset):
            style = ProjectStyle(_style)

        favourite = d.pop("favourite", UNSET)

        is_private = d.pop("isPrivate", UNSET)

        issue_type_hierarchy = None

        permissions = None

        properties: Union[ProjectProperties, Unset] = UNSET
        _properties = d.pop("properties", UNSET)
        if not isinstance(_properties, Unset):
            properties = ProjectProperties.from_dict(_properties)

        uuid = d.pop("uuid", UNSET)

        insight = None

        deleted = d.pop("deleted", UNSET)

        retention_till_date: Union[Unset, datetime.datetime] = UNSET
        _retention_till_date = d.pop("retentionTillDate", UNSET)
        if not isinstance(_retention_till_date, Unset):
            retention_till_date = isoparse(_retention_till_date)

        deleted_date: Union[Unset, datetime.datetime] = UNSET
        _deleted_date = d.pop("deletedDate", UNSET)
        if not isinstance(_deleted_date, Unset):
            deleted_date = isoparse(_deleted_date)

        deleted_by = None

        archived = d.pop("archived", UNSET)

        archived_date: Union[Unset, datetime.datetime] = UNSET
        _archived_date = d.pop("archivedDate", UNSET)
        if not isinstance(_archived_date, Unset):
            archived_date = isoparse(_archived_date)

        archived_by = None

        project = cls(
            expand=expand,
            self_=self_,
            id=id,
            key=key,
            description=description,
            lead=lead,
            components=components,
            issue_types=issue_types,
            url=url,
            email=email,
            assignee_type=assignee_type,
            versions=versions,
            name=name,
            roles=roles,
            avatar_urls=avatar_urls,
            project_category=project_category,
            project_type_key=project_type_key,
            simplified=simplified,
            style=style,
            favourite=favourite,
            is_private=is_private,
            issue_type_hierarchy=issue_type_hierarchy,
            permissions=permissions,
            properties=properties,
            uuid=uuid,
            insight=insight,
            deleted=deleted,
            retention_till_date=retention_till_date,
            deleted_date=deleted_date,
            deleted_by=deleted_by,
            archived=archived,
            archived_date=archived_date,
            archived_by=archived_by,
        )

        return project
