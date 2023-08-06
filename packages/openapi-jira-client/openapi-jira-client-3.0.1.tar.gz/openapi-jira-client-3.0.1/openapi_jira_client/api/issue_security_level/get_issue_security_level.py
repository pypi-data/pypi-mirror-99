from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.security_level import SecurityLevel
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/securitylevel/{id}".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[SecurityLevel, None, None]]:
    if response.status_code == 200:
        response_200 = SecurityLevel.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[SecurityLevel, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Response[Union[SecurityLevel, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Optional[Union[SecurityLevel, None, None]]:
    """Returns details of an issue security level.

    Use [Get issue security scheme](#api-rest-api-3-issuesecurityschemes-id-get) to obtain the IDs of issue security levels associated with the issue security scheme.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        id_=id_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Response[Union[SecurityLevel, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Optional[Union[SecurityLevel, None, None]]:
    """Returns details of an issue security level.

    Use [Get issue security scheme](#api-rest-api-3-issuesecurityschemes-id-get) to obtain the IDs of issue security levels associated with the issue security scheme.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
        )
    ).parsed
