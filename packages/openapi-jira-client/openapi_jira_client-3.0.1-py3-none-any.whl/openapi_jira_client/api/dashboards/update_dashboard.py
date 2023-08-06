from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.dashboard import Dashboard
from ...models.dashboard_details import DashboardDetails
from ...models.error_collection import ErrorCollection
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: DashboardDetails,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/dashboard/{id}".format(client.base_url, id=id_)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Dashboard, ErrorCollection, ErrorCollection, ErrorCollection]]:
    if response.status_code == 200:
        response_200 = Dashboard.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorCollection.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = ErrorCollection.from_dict(response.json())

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Dashboard, ErrorCollection, ErrorCollection, ErrorCollection]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: DashboardDetails,
) -> Response[Union[Dashboard, ErrorCollection, ErrorCollection, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: DashboardDetails,
) -> Optional[Union[Dashboard, ErrorCollection, ErrorCollection, ErrorCollection]]:
    """Updates a dashboard, replacing all the dashboard details with those provided.

    **[Permissions](#permissions) required:** None

    The dashboard to be updated must be owned by the user."""

    return sync_detailed(
        client=client,
        id_=id_,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: DashboardDetails,
) -> Response[Union[Dashboard, ErrorCollection, ErrorCollection, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: DashboardDetails,
) -> Optional[Union[Dashboard, ErrorCollection, ErrorCollection, ErrorCollection]]:
    """Updates a dashboard, replacing all the dashboard details with those provided.

    **[Permissions](#permissions) required:** None

    The dashboard to be updated must be owned by the user."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            json_body=json_body,
        )
    ).parsed
