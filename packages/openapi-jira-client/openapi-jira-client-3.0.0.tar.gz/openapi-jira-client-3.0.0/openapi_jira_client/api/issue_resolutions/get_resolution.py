from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.resolution import Resolution
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/resolution/{id}".format(client.base_url, id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Resolution, None, None]]:
    if response.status_code == 200:
        response_200 = Resolution.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Resolution, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id: str,
) -> Response[Union[Resolution, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id: str,
) -> Optional[Union[Resolution, None, None]]:
    """Returns an issue resolution value.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        id=id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id: str,
) -> Response[Union[Resolution, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id: str,
) -> Optional[Union[Resolution, None, None]]:
    """Returns an issue resolution value.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            id=id,
        )
    ).parsed
