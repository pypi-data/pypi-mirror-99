from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.issue_bean import IssueBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_fields: Union[Unset, List[str]] = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    json_properties: Union[Unset, List[str]] = UNSET
    if not isinstance(properties, Unset):
        json_properties = properties

    params: Dict[str, Any] = {
        "fields": json_fields,
        "fieldsByKeys": fields_by_keys,
        "expand": expand,
        "properties": json_properties,
        "updateHistory": update_history,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueBean, None, None]]:
    if response.status_code == 200:
        response_200 = IssueBean.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[IssueBean, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Response[Union[IssueBean, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        fields=fields,
        fields_by_keys=fields_by_keys,
        expand=expand,
        properties=properties,
        update_history=update_history,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Optional[Union[IssueBean, None, None]]:
    """Returns the details for an issue.

    The issue is identified by its ID or key, however, if the identifier doesn't match an issue, a case-insensitive search and check for moved issues is performed. If a matching issue is found its details are returned, a 302 or other redirect is **not** returned. The issue key returned in the response is the key of the issue found.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        fields=fields,
        fields_by_keys=fields_by_keys,
        expand=expand,
        properties=properties,
        update_history=update_history,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Response[Union[IssueBean, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        fields=fields,
        fields_by_keys=fields_by_keys,
        expand=expand,
        properties=properties,
        update_history=update_history,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Optional[Union[IssueBean, None, None]]:
    """Returns the details for an issue.

    The issue is identified by its ID or key, however, if the identifier doesn't match an issue, a case-insensitive search and check for moved issues is performed. If a matching issue is found its details are returned, a 302 or other redirect is **not** returned. The issue key returned in the response is the key of the issue found.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            fields=fields,
            fields_by_keys=fields_by_keys,
            expand=expand,
            properties=properties,
            update_history=update_history,
        )
    ).parsed
