from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.project_email_address import ProjectEmailAddress
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id: int,
    json_body: ProjectEmailAddress,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectId}/email".format(client.base_url, projectId=project_id)

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
    project_id: int,
    json_body: ProjectEmailAddress,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id=project_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id: int,
    json_body: ProjectEmailAddress,
) -> Optional[Union[None, None, None, None, None]]:
    """Sets the [project's sender email address](https://confluence.atlassian.com/x/dolKLg).

    If `emailAddress` is an empty string, the default email address is restored.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return sync_detailed(
        client=client,
        project_id=project_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: int,
    json_body: ProjectEmailAddress,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id=project_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: int,
    json_body: ProjectEmailAddress,
) -> Optional[Union[None, None, None, None, None]]:
    """Sets the [project's sender email address](https://confluence.atlassian.com/x/dolKLg).

    If `emailAddress` is an empty string, the default email address is restored.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            json_body=json_body,
        )
    ).parsed
