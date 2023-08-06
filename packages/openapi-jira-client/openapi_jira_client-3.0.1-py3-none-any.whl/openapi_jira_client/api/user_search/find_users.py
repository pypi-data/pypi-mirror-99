from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    property_: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query": query,
        "username": username,
        "accountId": account_id,
        "startAt": start_at,
        "maxResults": max_results,
        "property": property_,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[User], None, None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = User.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[User], None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    property_: Union[Unset, str] = UNSET,
) -> Response[Union[List[User], None, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        username=username,
        account_id=account_id,
        start_at=start_at,
        max_results=max_results,
        property_=property_,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    property_: Union[Unset, str] = UNSET,
) -> Optional[Union[List[User], None, None]]:
    """Returns a list of users that match the search string and property.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that match the search string and property. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who match the search string and property, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg). Anonymous calls or calls by users without the required permission return empty search results."""

    return sync_detailed(
        client=client,
        query=query,
        username=username,
        account_id=account_id,
        start_at=start_at,
        max_results=max_results,
        property_=property_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    property_: Union[Unset, str] = UNSET,
) -> Response[Union[List[User], None, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        username=username,
        account_id=account_id,
        start_at=start_at,
        max_results=max_results,
        property_=property_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    property_: Union[Unset, str] = UNSET,
) -> Optional[Union[List[User], None, None]]:
    """Returns a list of users that match the search string and property.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that match the search string and property. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who match the search string and property, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg). Anonymous calls or calls by users without the required permission return empty search results."""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            username=username,
            account_id=account_id,
            start_at=start_at,
            max_results=max_results,
            property_=property_,
        )
    ).parsed
