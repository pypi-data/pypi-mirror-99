from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.operation_message import OperationMessage
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey}".format(
        client.base_url, addonKey=addon_key, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[None, OperationMessage, OperationMessage, OperationMessage]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 400:
        response_400 = OperationMessage.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = OperationMessage.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = OperationMessage.from_dict(response.json())

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[None, OperationMessage, OperationMessage, OperationMessage]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
) -> Response[Union[None, OperationMessage, OperationMessage, OperationMessage]]:
    kwargs = _get_kwargs(
        client=client,
        addon_key=addon_key,
        property_key=property_key,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
) -> Optional[Union[None, OperationMessage, OperationMessage, OperationMessage]]:
    """Deletes an app's property.

    **[Permissions](#permissions) required:** Only a Connect app whose key matches `addonKey` can make this request."""

    return sync_detailed(
        client=client,
        addon_key=addon_key,
        property_key=property_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
) -> Response[Union[None, OperationMessage, OperationMessage, OperationMessage]]:
    kwargs = _get_kwargs(
        client=client,
        addon_key=addon_key,
        property_key=property_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
) -> Optional[Union[None, OperationMessage, OperationMessage, OperationMessage]]:
    """Deletes an app's property.

    **[Permissions](#permissions) required:** Only a Connect app whose key matches `addonKey` can make this request."""

    return (
        await asyncio_detailed(
            client=client,
            addon_key=addon_key,
            property_key=property_key,
        )
    ).parsed
