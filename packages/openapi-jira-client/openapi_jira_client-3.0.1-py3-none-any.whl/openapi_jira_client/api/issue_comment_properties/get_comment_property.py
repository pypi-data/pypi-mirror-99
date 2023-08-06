from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.entity_property import EntityProperty
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/comment/{commentId}/properties/{propertyKey}".format(
        client.base_url, commentId=comment_id, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EntityProperty, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = EntityProperty.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[EntityProperty, None, None, None, None]]:
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
) -> Response[Union[EntityProperty, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        comment_id=comment_id,
        property_key=property_key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
) -> Optional[Union[EntityProperty, None, None, None, None]]:
    """Returns the value of a comment property.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return sync_detailed(
        client=client,
        comment_id=comment_id,
        property_key=property_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
) -> Response[Union[EntityProperty, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        comment_id=comment_id,
        property_key=property_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    comment_id: str,
    property_key: str,
) -> Optional[Union[EntityProperty, None, None, None, None]]:
    """Returns the value of a comment property.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            comment_id=comment_id,
            property_key=property_key,
        )
    ).parsed
