from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.status_details import StatusDetails
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/status/{idOrName}".format(client.base_url, idOrName=id_or_name)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[StatusDetails, None, None]]:
    if response.status_code == 200:
        response_200 = StatusDetails.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[StatusDetails, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Response[Union[StatusDetails, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_or_name=id_or_name,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Optional[Union[StatusDetails, None, None]]:
    """Returns a status. The status must be associated with a workflow to be returned.

    If a name is used on more than one status, only the status found first is returned. Therefore, identifying the status by its ID may be preferable.

    This operation can be accessed anonymously.

    [Permissions](#permissions) required: None."""

    return sync_detailed(
        client=client,
        id_or_name=id_or_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Response[Union[StatusDetails, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_or_name=id_or_name,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Optional[Union[StatusDetails, None, None]]:
    """Returns a status. The status must be associated with a workflow to be returned.

    If a name is used on more than one status, only the status found first is returned. Therefore, identifying the status by its ID may be preferable.

    This operation can be accessed anonymously.

    [Permissions](#permissions) required: None."""

    return (
        await asyncio_detailed(
            client=client,
            id_or_name=id_or_name,
        )
    ).parsed
