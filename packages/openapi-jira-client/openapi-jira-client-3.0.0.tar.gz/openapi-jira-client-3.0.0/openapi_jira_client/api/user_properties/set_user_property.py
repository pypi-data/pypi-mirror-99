from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/properties/{propertyKey}".format(client.base_url, propertyKey=property_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "accountId": account_id,
        "userKey": user_key,
        "username": username,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = None

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 201:
        response_201 = None

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
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 405:
        response_405 = None

        return response_405
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        json_body=json_body,
        account_id=account_id,
        user_key=user_key,
        username=username,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None, None, None]]:
    """Sets the value of a user's property. Use this resource to store custom data against a user.

    Note: This operation does not access the [user properties](https://confluence.atlassian.com/x/8YxjL) created and maintained in Jira.

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg), to set a property on any user.
     *  Access to Jira, to set a property on the calling user's record."""

    return sync_detailed(
        client=client,
        property_key=property_key,
        json_body=json_body,
        account_id=account_id,
        user_key=user_key,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        json_body=json_body,
        account_id=account_id,
        user_key=user_key,
        username=username,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None, None, None]]:
    """Sets the value of a user's property. Use this resource to store custom data against a user.

    Note: This operation does not access the [user properties](https://confluence.atlassian.com/x/8YxjL) created and maintained in Jira.

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg), to set a property on any user.
     *  Access to Jira, to set a property on the calling user's record."""

    return (
        await asyncio_detailed(
            client=client,
            property_key=property_key,
            json_body=json_body,
            account_id=account_id,
            user_key=user_key,
            username=username,
        )
    ).parsed
