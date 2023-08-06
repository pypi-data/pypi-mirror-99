from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.permissions_keys_bean import PermissionsKeysBean
from ...models.permitted_projects import PermittedProjects
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: PermissionsKeysBean,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissions/project".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[PermittedProjects, None, None]]:
    if response.status_code == 200:
        response_200 = PermittedProjects.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PermittedProjects, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PermissionsKeysBean,
) -> Response[Union[PermittedProjects, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: PermissionsKeysBean,
) -> Optional[Union[PermittedProjects, None, None]]:
    """Returns all the projects where the user is granted a list of project permissions.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PermissionsKeysBean,
) -> Response[Union[PermittedProjects, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: PermissionsKeysBean,
) -> Optional[Union[PermittedProjects, None, None]]:
    """Returns all the projects where the user is granted a list of project permissions.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
