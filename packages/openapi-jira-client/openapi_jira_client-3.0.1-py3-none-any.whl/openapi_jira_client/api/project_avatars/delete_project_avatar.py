from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/avatar/{id}".format(
        client.base_url, projectIdOrKey=project_id_or_key, id=id_
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
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
    project_id_or_key: str,
    id_: int,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
) -> Optional[Union[None, None, None, None]]:
    """Deletes a custom avatar from a project. Note that system avatars cannot be deleted.

    **[Permissions](#permissions) required:** *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg)."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
) -> Optional[Union[None, None, None, None]]:
    """Deletes a custom avatar from a project. Note that system avatars cannot be deleted.

    **[Permissions](#permissions) required:** *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            id_=id_,
        )
    ).parsed
