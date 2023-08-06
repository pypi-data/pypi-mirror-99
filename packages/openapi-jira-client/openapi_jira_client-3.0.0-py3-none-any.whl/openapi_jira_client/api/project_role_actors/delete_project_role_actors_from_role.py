from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.project_role import ProjectRole
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/role/{id}/actors".format(client.base_url, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ProjectRole, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = ProjectRole.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[ProjectRole, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Response[Union[ProjectRole, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
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
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Optional[Union[ProjectRole, None, None, None, None]]:
    """Deletes the [default actors](#api-rest-api-3-resolution-get) from a project role. You may delete a group or user, but you cannot delete a group and a user in the same request.

    Changing a project role's default actors does not affect project role members for projects already created.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id=id,
        user=user,
        group=group,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Response[Union[ProjectRole, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
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
    id: int,
    user: Union[Unset, str] = UNSET,
    group: Union[Unset, str] = UNSET,
) -> Optional[Union[ProjectRole, None, None, None, None]]:
    """Deletes the [default actors](#api-rest-api-3-resolution-get) from a project role. You may delete a group or user, but you cannot delete a group and a user in the same request.

    Changing a project role's default actors does not affect project role members for projects already created.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            user=user,
            group=group,
        )
    ).parsed
