from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.permission_grant import PermissionGrant
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionGrant,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissionscheme/{schemeId}/permission".format(client.base_url, schemeId=scheme_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "expand": expand,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[PermissionGrant, None, None, None]]:
    if response.status_code == 201:
        response_201 = PermissionGrant.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PermissionGrant, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionGrant,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[PermissionGrant, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        json_body=json_body,
        expand=expand,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionGrant,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[PermissionGrant, None, None, None]]:
    """Creates a permission grant in a permission scheme.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        scheme_id=scheme_id,
        json_body=json_body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionGrant,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[PermissionGrant, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        json_body=json_body,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionGrant,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[PermissionGrant, None, None, None]]:
    """Creates a permission grant in a permission scheme.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            scheme_id=scheme_id,
            json_body=json_body,
            expand=expand,
        )
    ).parsed
