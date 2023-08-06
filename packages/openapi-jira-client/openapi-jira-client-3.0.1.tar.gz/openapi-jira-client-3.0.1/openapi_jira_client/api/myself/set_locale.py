from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.locale import Locale
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: Locale,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/mypreferences/locale".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
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
    json_body: Locale,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: Locale,
) -> Optional[Union[None, None, None]]:
    """Deprecated, use [ Update a user profile](https://developer.atlassian.com/cloud/admin/user-management/rest/#api-users-account-id-manage-profile-patch) from the user management REST API instead.

    Sets the locale of the user. The locale must be one supported by the instance of Jira.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Locale,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: Locale,
) -> Optional[Union[None, None, None]]:
    """Deprecated, use [ Update a user profile](https://developer.atlassian.com/cloud/admin/user-management/rest/#api-users-account-id-manage-profile-patch) from the user management REST API instead.

    Sets the locale of the user. The locale must be one supported by the instance of Jira.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
