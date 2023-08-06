from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.delete_avatar_type import DeleteAvatarType
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/universal_avatar/type/{type}/owner/{owningObjectId}/avatar/{id}".format(
        client.base_url, type=type_, owningObjectId=owning_object_id, id=id_
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
    if response.status_code == 400:
        response_400 = None

        return response_400
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
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        owning_object_id=owning_object_id,
        id_=id_,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Optional[Union[None, None, None, None]]:
    """Deletes an avatar from a project or issue type.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        type_=type_,
        owning_object_id=owning_object_id,
        id_=id_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        owning_object_id=owning_object_id,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Optional[Union[None, None, None, None]]:
    """Deletes an avatar from a project or issue type.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            type_=type_,
            owning_object_id=owning_object_id,
            id_=id_,
        )
    ).parsed
