from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.actors_map import ActorsMap
from ...models.project_role import ProjectRole
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
    json_body: ActorsMap,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/role/{id}".format(
        client.base_url, projectIdOrKey=project_id_or_key, id=id_
    )

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ProjectRole, None, None, None]]:
    if response.status_code == 200:
        response_200 = ProjectRole.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[ProjectRole, None, None, None]]:
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
    id_: int,
    json_body: ActorsMap,
) -> Response[Union[ProjectRole, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
    json_body: ActorsMap,
) -> Optional[Union[ProjectRole, None, None, None]]:
    """Adds actors to a project role for the project.

    To replace all actors for the project, use [Set actors for project role](#api-rest-api-3-project-projectIdOrKey-role-id-put).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project or *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
    json_body: ActorsMap,
) -> Response[Union[ProjectRole, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
    json_body: ActorsMap,
) -> Optional[Union[ProjectRole, None, None, None]]:
    """Adds actors to a project role for the project.

    To replace all actors for the project, use [Set actors for project role](#api-rest-api-3-project-projectIdOrKey-role-id-put).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project or *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            id_=id_,
            json_body=json_body,
        )
    ).parsed
