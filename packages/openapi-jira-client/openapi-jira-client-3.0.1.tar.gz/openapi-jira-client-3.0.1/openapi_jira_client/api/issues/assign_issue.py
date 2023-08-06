from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.user import User
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: User,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/assignee".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None]]:
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
    json_body: User,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
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
    json_body: User,
) -> Optional[Union[None, None, None, None]]:
    """Assigns an issue to a user. Use this operation when the calling user does not have the *Edit Issues* permission but has the *Assign issue* permission for the project that the issue is in.

    If `name` or `accountId` is set to:

     *  `\"-1\"`, the issue is assigned to the default assignee for the project.
     *  `null`, the issue is set to unassigned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse Projects* and *Assign Issues* [ project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: User,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: User,
) -> Optional[Union[None, None, None, None]]:
    """Assigns an issue to a user. Use this operation when the calling user does not have the *Edit Issues* permission but has the *Assign issue* permission for the project that the issue is in.

    If `name` or `accountId` is set to:

     *  `\"-1\"`, the issue is assigned to the default assignee for the project.
     *  `null`, the issue is set to unassigned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse Projects* and *Assign Issues* [ project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            json_body=json_body,
        )
    ).parsed
