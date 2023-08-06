from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/filter/{id}/columns".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None]]:
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
) -> Response[Union[None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
) -> Optional[Union[None, None]]:
    """Sets the columns for a filter. Only navigable fields can be set as columns. Use [Get fields](#api-rest-api-3-field-get) to get the list fields in Jira. A navigable field has `navigable` set to `true`.

    The parameters for this resource are expressed as HTML form data. For example, in curl:

    `curl -X PUT -d columns=summary -d columns=description https://your-domain.atlassian.net/rest/api/3/filter/10000/columns`

    **[Permissions](#permissions) required:** Permission to access Jira, however, columns are only set for:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

    return sync_detailed(
        client=client,
        id_=id_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
) -> Response[Union[None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
) -> Optional[Union[None, None]]:
    """Sets the columns for a filter. Only navigable fields can be set as columns. Use [Get fields](#api-rest-api-3-field-get) to get the list fields in Jira. A navigable field has `navigable` set to `true`.

    The parameters for this resource are expressed as HTML form data. For example, in curl:

    `curl -X PUT -d columns=summary -d columns=description https://your-domain.atlassian.net/rest/api/3/filter/10000/columns`

    **[Permissions](#permissions) required:** Permission to access Jira, however, columns are only set for:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
        )
    ).parsed
