from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id: str,
    move_fix_issues_to: Union[Unset, str] = UNSET,
    move_affected_issues_to: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/version/{id}".format(client.base_url, id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "moveFixIssuesTo": move_fix_issues_to,
        "moveAffectedIssuesTo": move_affected_issues_to,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id: str,
    move_fix_issues_to: Union[Unset, str] = UNSET,
    move_affected_issues_to: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        move_fix_issues_to=move_fix_issues_to,
        move_affected_issues_to=move_affected_issues_to,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id: str,
    move_fix_issues_to: Union[Unset, str] = UNSET,
    move_affected_issues_to: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None]]:
    """Deletes a project version.

    Deprecated, use [ Delete and replace version](#api-rest-api-3-version-id-removeAndSwap-post) that supports swapping version values in custom fields, in addition to the swapping for `fixVersion` and `affectedVersion` provided in this resource.

    Alternative versions can be provided to update issues that use the deleted version in `fixVersion` or `affectedVersion`. If alternatives are not provided, occurrences of `fixVersion` and `affectedVersion` that contain the deleted version are cleared.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that contains the version."""

    return sync_detailed(
        client=client,
        id=id,
        move_fix_issues_to=move_fix_issues_to,
        move_affected_issues_to=move_affected_issues_to,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id: str,
    move_fix_issues_to: Union[Unset, str] = UNSET,
    move_affected_issues_to: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        move_fix_issues_to=move_fix_issues_to,
        move_affected_issues_to=move_affected_issues_to,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id: str,
    move_fix_issues_to: Union[Unset, str] = UNSET,
    move_affected_issues_to: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None]]:
    """Deletes a project version.

    Deprecated, use [ Delete and replace version](#api-rest-api-3-version-id-removeAndSwap-post) that supports swapping version values in custom fields, in addition to the swapping for `fixVersion` and `affectedVersion` provided in this resource.

    Alternative versions can be provided to update issues that use the deleted version in `fixVersion` or `affectedVersion`. If alternatives are not provided, occurrences of `fixVersion` and `affectedVersion` that contain the deleted version are cleared.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that contains the version."""

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            move_fix_issues_to=move_fix_issues_to,
            move_affected_issues_to=move_affected_issues_to,
        )
    ).parsed
