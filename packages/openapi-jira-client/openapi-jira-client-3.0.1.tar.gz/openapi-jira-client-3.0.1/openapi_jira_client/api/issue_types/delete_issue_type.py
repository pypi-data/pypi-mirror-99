from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: str,
    alternative_issue_type_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issuetype/{id}".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "alternativeIssueTypeId": alternative_issue_type_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
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
    if response.status_code == 409:
        response_409 = None

        return response_409
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
    id_: str,
    alternative_issue_type_id: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        alternative_issue_type_id=alternative_issue_type_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: str,
    alternative_issue_type_id: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Deletes the issue type. If the issue type is in use, all uses are updated with the alternative issue type (`alternativeIssueTypeId`). A list of alternative issue types are obtained from the [Get alternative issue types](#api-rest-api-3-issuetype-id-alternatives-get) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id_=id_,
        alternative_issue_type_id=alternative_issue_type_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
    alternative_issue_type_id: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        alternative_issue_type_id=alternative_issue_type_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: str,
    alternative_issue_type_id: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Deletes the issue type. If the issue type is in use, all uses are updated with the alternative issue type (`alternativeIssueTypeId`). A list of alternative issue types are obtained from the [Get alternative issue types](#api-rest-api-3-issuetype-id-alternatives-get) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            alternative_issue_type_id=alternative_issue_type_id,
        )
    ).parsed
