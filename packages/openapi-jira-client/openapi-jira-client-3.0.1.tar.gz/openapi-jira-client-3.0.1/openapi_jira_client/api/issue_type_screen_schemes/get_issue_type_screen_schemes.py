from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.page_bean_issue_type_screen_scheme import PageBeanIssueTypeScreenScheme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    id_: Union[Unset, List[int]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issuetypescreenscheme".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_id_: Union[Unset, List[int]] = UNSET
    if not isinstance(id_, Unset):
        json_id_ = id_

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "id": json_id_,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[PageBeanIssueTypeScreenScheme, None, None, None]]:
    if response.status_code == 200:
        response_200 = PageBeanIssueTypeScreenScheme.from_dict(response.json())

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
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PageBeanIssueTypeScreenScheme, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    id_: Union[Unset, List[int]] = UNSET,
) -> Response[Union[PageBeanIssueTypeScreenScheme, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        id_=id_,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    id_: Union[Unset, List[int]] = UNSET,
) -> Optional[Union[PageBeanIssueTypeScreenScheme, None, None, None]]:
    """Returns a [paginated](#pagination) list of issue type screen schemes.

    Only issue type screen schemes used in classic projects are returned.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        id_=id_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    id_: Union[Unset, List[int]] = UNSET,
) -> Response[Union[PageBeanIssueTypeScreenScheme, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    id_: Union[Unset, List[int]] = UNSET,
) -> Optional[Union[PageBeanIssueTypeScreenScheme, None, None, None]]:
    """Returns a [paginated](#pagination) list of issue type screen schemes.

    Only issue type screen schemes used in classic projects are returned.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            id_=id_,
        )
    ).parsed
