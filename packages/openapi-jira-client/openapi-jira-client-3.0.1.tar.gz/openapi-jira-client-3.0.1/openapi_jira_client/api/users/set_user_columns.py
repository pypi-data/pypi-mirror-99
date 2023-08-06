from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/columns".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "accountId": account_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 500:
        response_500 = None

        return response_500
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
    account_id: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None]]:
    """Sets the default [ issue table columns](https://confluence.atlassian.com/x/XYdKLg) for the user. If an account ID is not passed, the calling user's default columns are set. If no column details are sent, then all default columns are removed.

    The parameters for this resource are expressed as HTML form data. For example, in curl:

    `curl -X PUT -d columns=summary -d columns=description https://your-domain.atlassian.net/rest/api/3/user/columns?accountId=5b10ac8d82e05b22cc7d4ef5'`

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg), to set the columns on any user.
     *  Permission to access Jira, to set the calling user's columns."""

    return sync_detailed(
        client=client,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None]]:
    """Sets the default [ issue table columns](https://confluence.atlassian.com/x/XYdKLg) for the user. If an account ID is not passed, the calling user's default columns are set. If no column details are sent, then all default columns are removed.

    The parameters for this resource are expressed as HTML form data. For example, in curl:

    `curl -X PUT -d columns=summary -d columns=description https://your-domain.atlassian.net/rest/api/3/user/columns?accountId=5b10ac8d82e05b22cc7d4ef5'`

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg), to set the columns on any user.
     *  Permission to access Jira, to set the calling user's columns."""

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
        )
    ).parsed
