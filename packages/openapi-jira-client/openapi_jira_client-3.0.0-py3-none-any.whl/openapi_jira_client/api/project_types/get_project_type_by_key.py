from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.get_project_type_by_key_project_type_key import GetProjectTypeByKeyProjectTypeKey
from ...models.project_type import ProjectType
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_type_key: GetProjectTypeByKeyProjectTypeKey,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/type/{projectTypeKey}".format(client.base_url, projectTypeKey=project_type_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ProjectType, None, None]]:
    if response.status_code == 200:
        response_200 = ProjectType.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ProjectType, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_type_key: GetProjectTypeByKeyProjectTypeKey,
) -> Response[Union[ProjectType, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_type_key=project_type_key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_type_key: GetProjectTypeByKeyProjectTypeKey,
) -> Optional[Union[ProjectType, None, None]]:
    """Returns a [project type](https://confluence.atlassian.com/x/Var1Nw).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        project_type_key=project_type_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_type_key: GetProjectTypeByKeyProjectTypeKey,
) -> Response[Union[ProjectType, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_type_key=project_type_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_type_key: GetProjectTypeByKeyProjectTypeKey,
) -> Optional[Union[ProjectType, None, None]]:
    """Returns a [project type](https://confluence.atlassian.com/x/Var1Nw).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            project_type_key=project_type_key,
        )
    ).parsed
