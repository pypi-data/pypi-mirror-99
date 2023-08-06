from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}".format(
        client.base_url, dashboardId=dashboard_id, itemId=item_id, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
        property_key=property_key,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes a dashboard item property.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The user must be the owner of the dashboard. Note, users with the *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) are considered owners of the System dashboard."""

    return sync_detailed(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
        property_key=property_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
        property_key=property_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes a dashboard item property.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The user must be the owner of the dashboard. Note, users with the *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) are considered owners of the System dashboard."""

    return (
        await asyncio_detailed(
            client=client,
            dashboard_id=dashboard_id,
            item_id=item_id,
            property_key=property_key,
        )
    ).parsed
