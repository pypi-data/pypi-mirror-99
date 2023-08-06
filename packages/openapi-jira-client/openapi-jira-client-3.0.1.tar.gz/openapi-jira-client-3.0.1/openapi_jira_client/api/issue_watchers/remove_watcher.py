from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/watchers".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "username": username,
        "accountId": account_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None]]:
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
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        username=username,
        account_id=account_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes a user as a watcher of an issue.

    This operation requires the **Allow users to watch issues** option to be *ON*. This option is set in General configuration for Jira. See [Configuring Jira application options](https://confluence.atlassian.com/x/uYXKM) for details.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  To remove users other than themselves from the watchlist, *Manage watcher list* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        username=username,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        username=username,
        account_id=account_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes a user as a watcher of an issue.

    This operation requires the **Allow users to watch issues** option to be *ON*. This option is set in General configuration for Jira. See [Configuring Jira application options](https://confluence.atlassian.com/x/uYXKM) for details.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  To remove users other than themselves from the watchlist, *Manage watcher list* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            username=username,
            account_id=account_id,
        )
    ).parsed
