from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.search_request_bean import SearchRequestBean
from ...models.search_results import SearchResults
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: SearchRequestBean,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/search".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[SearchResults, None, None]]:
    if response.status_code == 200:
        response_200 = SearchResults.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[SearchResults, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SearchRequestBean,
) -> Response[Union[SearchResults, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: SearchRequestBean,
) -> Optional[Union[SearchResults, None, None]]:
    """Searches for issues using [JQL](https://confluence.atlassian.com/x/egORLQ).

    There is a [GET](#api-rest-api-3-search-get) version of this resource that can be used for smaller JQL query expressions.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Issues are included in the response where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the issue.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SearchRequestBean,
) -> Response[Union[SearchResults, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: SearchRequestBean,
) -> Optional[Union[SearchResults, None, None]]:
    """Searches for issues using [JQL](https://confluence.atlassian.com/x/egORLQ).

    There is a [GET](#api-rest-api-3-search-get) version of this resource that can be used for smaller JQL query expressions.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Issues are included in the response where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the issue.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
