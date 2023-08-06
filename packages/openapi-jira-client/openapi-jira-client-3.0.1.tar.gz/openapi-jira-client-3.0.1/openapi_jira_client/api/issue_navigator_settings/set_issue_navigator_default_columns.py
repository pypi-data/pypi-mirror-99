from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/settings/columns".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = None

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
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[None, None, None, None, None]]:
    """Sets the default issue navigator columns.

    The `columns` parameter accepts a navigable field value and is expressed as HTML form data. To specify multiple columns, pass multiple `columns` parameters. For example, in curl:

    `curl -X PUT -d columns=summary -d columns=description https://your-domain.atlassian.net/rest/api/3/settings/columns`

    If no column details are sent, then all default columns are removed.

    A navigable field is one that can be used as a column on the issue navigator. Find details of navigable issue columns using [Get fields](#api-rest-api-3-field-get).

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[None, None, None, None, None]]:
    """Sets the default issue navigator columns.

    The `columns` parameter accepts a navigable field value and is expressed as HTML form data. To specify multiple columns, pass multiple `columns` parameters. For example, in curl:

    `curl -X PUT -d columns=summary -d columns=description https://your-domain.atlassian.net/rest/api/3/settings/columns`

    If no column details are sent, then all default columns are removed.

    A navigable field is one that can be used as a column on the issue navigator. Find details of navigable issue columns using [Get fields](#api-rest-api-3-field-get).

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
