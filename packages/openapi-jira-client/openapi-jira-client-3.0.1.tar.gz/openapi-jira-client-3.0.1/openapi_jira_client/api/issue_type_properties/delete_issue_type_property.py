from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_type_id: str,
    property_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey}".format(
        client.base_url, issueTypeId=issue_type_id, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None]]:
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
    issue_type_id: str,
    property_key: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_type_id=issue_type_id,
        property_key=property_key,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_type_id: str,
    property_key: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes the [issue type property](https://developer.atlassian.com/cloud/jira/platform/storing-data-without-a-database/#a-id-jira-entity-properties-a-jira-entity-properties).

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        issue_type_id=issue_type_id,
        property_key=property_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_type_id: str,
    property_key: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_type_id=issue_type_id,
        property_key=property_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_type_id: str,
    property_key: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes the [issue type property](https://developer.atlassian.com/cloud/jira/platform/storing-data-without-a-database/#a-id-jira-entity-properties-a-jira-entity-properties).

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            issue_type_id=issue_type_id,
            property_key=property_key,
        )
    ).parsed
