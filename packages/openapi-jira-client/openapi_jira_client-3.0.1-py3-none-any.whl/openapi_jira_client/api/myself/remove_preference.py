from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/mypreferences".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "key": key,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Optional[Union[None, None, None]]:
    """Deletes a preference of the user, which restores the default value of system defined settings.

    Note that these keys are deprecated:

     *  *jira.user.locale* The locale of the user. By default, not set. The user takes the instance locale.
     *  *jira.user.timezone* The time zone of the user. By default, not set. The user takes the instance timezone.

    Use [ Update a user profile](https://developer.atlassian.com/cloud/admin/user-management/rest/#api-users-account-id-manage-profile-patch) from the user management REST API to manage timezone and locale instead.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        key=key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Optional[Union[None, None, None]]:
    """Deletes a preference of the user, which restores the default value of system defined settings.

    Note that these keys are deprecated:

     *  *jira.user.locale* The locale of the user. By default, not set. The user takes the instance locale.
     *  *jira.user.timezone* The time zone of the user. By default, not set. The user takes the instance timezone.

    Use [ Update a user profile](https://developer.atlassian.com/cloud/admin/user-management/rest/#api-users-account-id-manage-profile-patch) from the user management REST API to manage timezone and locale instead.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            key=key,
        )
    ).parsed
