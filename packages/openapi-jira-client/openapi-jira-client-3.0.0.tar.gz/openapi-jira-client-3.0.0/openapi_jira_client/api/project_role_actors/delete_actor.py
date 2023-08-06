from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/role/{id}".format(
        client.base_url, projectIdOrKey=project_id_or_key, id=id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "user": user,
        "group": group,
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
    if response.status_code == 400:
        response_400 = None

        return response_400
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
    project_id_or_key: str,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id=id,
        user=user,
        group=group,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None]]:
    """Deletes actors from a project role for the project.

    To remove default actors from the project role, use [Delete default actors from project role](#api-rest-api-3-role-id-actors-delete).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project or *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        id=id,
        user=user,
        group=group,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id=id,
        user=user,
        group=group,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None]]:
    """Deletes actors from a project role for the project.

    To remove default actors from the project role, use [Delete default actors from project role](#api-rest-api-3-role-id-actors-delete).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project or *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            id=id,
            user=user,
            group=group,
        )
    ).parsed
