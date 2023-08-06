from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    worklog_id: str,
    property_key: str,
    json_body: None,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey}".format(
        client.base_url, issueIdOrKey=issue_id_or_key, worklogId=worklog_id, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = None

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 201:
        response_201 = None

        return response_201
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None, None]]:
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
    worklog_id: str,
    property_key: str,
    json_body: None,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        worklog_id=worklog_id,
        property_key=property_key,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    worklog_id: str,
    property_key: str,
    json_body: None,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Sets the value of a worklog property. Use this operation to store custom data against the worklog.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Edit all worklogs*[ project permission](https://confluence.atlassian.com/x/yodKLg) to update any worklog or *Edit own worklogs* to update worklogs created by the user.
     *  If the worklog has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        worklog_id=worklog_id,
        property_key=property_key,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    worklog_id: str,
    property_key: str,
    json_body: None,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        worklog_id=worklog_id,
        property_key=property_key,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    worklog_id: str,
    property_key: str,
    json_body: None,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Sets the value of a worklog property. Use this operation to store custom data against the worklog.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Edit all worklogs*[ project permission](https://confluence.atlassian.com/x/yodKLg) to update any worklog or *Edit own worklogs* to update worklogs created by the user.
     *  If the worklog has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            worklog_id=worklog_id,
            property_key=property_key,
            json_body=json_body,
        )
    ).parsed
