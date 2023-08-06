from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.issue_bean import IssueBean
from ..models.search_results_names import SearchResultsNames
from ..models.search_results_schema import SearchResultsSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResults")


@attr.s(auto_attribs=True)
class SearchResults:
    """ The result of a JQL search. """

    expand: Union[Unset, str] = UNSET
    start_at: Union[Unset, int] = UNSET
    max_results: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    issues: Union[Unset, List[IssueBean]] = UNSET
    warning_messages: Union[Unset, List[str]] = UNSET
    names: Union[Unset, SearchResultsNames] = UNSET
    schema: Union[Unset, SearchResultsSchema] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        start_at = self.start_at
        max_results = self.max_results
        total = self.total
        issues: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = []
            for issues_item_data in self.issues:
                issues_item = issues_item_data.to_dict()

                issues.append(issues_item)

        warning_messages: Union[Unset, List[str]] = UNSET
        if not isinstance(self.warning_messages, Unset):
            warning_messages = self.warning_messages

        names: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.names, Unset):
            names = self.names.to_dict()

        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if total is not UNSET:
            field_dict["total"] = total
        if issues is not UNSET:
            field_dict["issues"] = issues
        if warning_messages is not UNSET:
            field_dict["warningMessages"] = warning_messages
        if names is not UNSET:
            field_dict["names"] = names
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        start_at = d.pop("startAt", UNSET)

        max_results = d.pop("maxResults", UNSET)

        total = d.pop("total", UNSET)

        issues = []
        _issues = d.pop("issues", UNSET)
        for issues_item_data in _issues or []:
            issues_item = IssueBean.from_dict(issues_item_data)

            issues.append(issues_item)

        warning_messages = cast(List[str], d.pop("warningMessages", UNSET))

        names: Union[Unset, SearchResultsNames] = UNSET
        _names = d.pop("names", UNSET)
        if not isinstance(_names, Unset):
            names = SearchResultsNames.from_dict(_names)

        schema: Union[Unset, SearchResultsSchema] = UNSET
        _schema = d.pop("schema", UNSET)
        if not isinstance(_schema, Unset):
            schema = SearchResultsSchema.from_dict(_schema)

        search_results = cls(
            expand=expand,
            start_at=start_at,
            max_results=max_results,
            total=total,
            issues=issues,
            warning_messages=warning_messages,
            names=names,
            schema=schema,
        )

        return search_results
