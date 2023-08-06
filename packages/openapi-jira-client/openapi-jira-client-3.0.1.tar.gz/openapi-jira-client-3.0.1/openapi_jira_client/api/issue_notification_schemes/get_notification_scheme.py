from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.notification_scheme import NotificationScheme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/notificationscheme/{id}".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "expand": expand,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[NotificationScheme, None, None, None]]:
    if response.status_code == 200:
        response_200 = NotificationScheme.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[NotificationScheme, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[NotificationScheme, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[NotificationScheme, None, None, None]]:
    """Returns a [notification scheme](https://confluence.atlassian.com/x/8YdKLg), including the list of events and the recipients who will receive notifications for those events.

    **[Permissions](#permissions) required:** Permission to access Jira, however the user must have permission to administer at least one project associated with the notification scheme."""

    return sync_detailed(
        client=client,
        id_=id_,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[NotificationScheme, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[NotificationScheme, None, None, None]]:
    """Returns a [notification scheme](https://confluence.atlassian.com/x/8YdKLg), including the list of events and the recipients who will receive notifications for those events.

    **[Permissions](#permissions) required:** Permission to access Jira, however the user must have permission to administer at least one project associated with the notification scheme."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            expand=expand,
        )
    ).parsed
