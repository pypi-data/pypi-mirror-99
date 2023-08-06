from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    property_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/properties/{propertyKey}".format(
        client.base_url, projectIdOrKey=project_id_or_key, propertyKey=property_key
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
    project_id_or_key: str,
    property_key: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        property_key=property_key,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    property_key: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes the [property](https://developer.atlassian.com/cloud/jira/platform/storing-data-without-a-database/#a-id-jira-entity-properties-a-jira-entity-properties) from a project.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the property."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        property_key=property_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    property_key: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        property_key=property_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    property_key: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes the [property](https://developer.atlassian.com/cloud/jira/platform/storing-data-without-a-database/#a-id-jira-entity-properties-a-jira-entity-properties) from a project.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the property."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            property_key=property_key,
        )
    ).parsed
