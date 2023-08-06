from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
    json_body: None,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/comment/{commentId}/properties/{propertyKey}".format(
        client.base_url, commentId=comment_id, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = None

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None, None]]:
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
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
    json_body: None,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        comment_id=comment_id,
        property_key=property_key,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
    json_body: None,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Creates or updates the value of a property for a comment. Use this resource to store custom data against a comment.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    **[Permissions](#permissions) required:** either of:

     *  *Edit All Comments* [project permission](https://confluence.atlassian.com/x/yodKLg) to create or update the value of a property on any comment.
     *  *Edit Own Comments* [project permission](https://confluence.atlassian.com/x/yodKLg) to create or update the value of a property on a comment created by the user.

    Also, when the visibility of a comment is restricted to a role or group the user must be a member of that role or group."""

    return sync_detailed(
        client=client,
        comment_id=comment_id,
        property_key=property_key,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
    json_body: None,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        comment_id=comment_id,
        property_key=property_key,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
    json_body: None,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Creates or updates the value of a property for a comment. Use this resource to store custom data against a comment.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    **[Permissions](#permissions) required:** either of:

     *  *Edit All Comments* [project permission](https://confluence.atlassian.com/x/yodKLg) to create or update the value of a property on any comment.
     *  *Edit Own Comments* [project permission](https://confluence.atlassian.com/x/yodKLg) to create or update the value of a property on a comment created by the user.

    Also, when the visibility of a comment is restricted to a role or group the user must be a member of that role or group."""

    return (
        await asyncio_detailed(
            client=client,
            comment_id=comment_id,
            property_key=property_key,
            json_body=json_body,
        )
    ).parsed
