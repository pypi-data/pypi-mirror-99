from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    global_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/remotelink".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "globalId": global_id,
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
    global_id: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        global_id=global_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    global_id: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes the remote issue link from the issue using the link's global ID. Where the global ID includes reserved URL characters these must be escaped in the request. For example, pass `system=http://www.mycompany.com/support&id=1` as `system%3Dhttp%3A%2F%2Fwww.mycompany.com%2Fsupport%26id%3D1`.

    This operation requires [issue linking to be active](https://confluence.atlassian.com/x/yoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Link issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is implemented, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        global_id=global_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    global_id: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        global_id=global_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    global_id: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes the remote issue link from the issue using the link's global ID. Where the global ID includes reserved URL characters these must be escaped in the request. For example, pass `system=http://www.mycompany.com/support&id=1` as `system%3Dhttp%3A%2F%2Fwww.mycompany.com%2Fsupport%26id%3D1`.

    This operation requires [issue linking to be active](https://confluence.atlassian.com/x/yoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Link issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is implemented, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            global_id=global_id,
        )
    ).parsed
