from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.create_custom_field_context import CreateCustomFieldContext
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: CreateCustomFieldContext,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context".format(client.base_url, fieldId=field_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[CreateCustomFieldContext, None, None, None, None]]:
    if response.status_code == 201:
        response_201 = CreateCustomFieldContext.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 409:
        response_409 = None

        return response_409
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[CreateCustomFieldContext, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: CreateCustomFieldContext,
) -> Response[Union[CreateCustomFieldContext, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: CreateCustomFieldContext,
) -> Optional[Union[CreateCustomFieldContext, None, None, None, None]]:
    """Creates a custom field context.

    If `projectIds` is empty, a global context is created. A global context is one that applies to all project. If `issueTypeIds` is empty, the context applies to all issue types.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        field_id=field_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: CreateCustomFieldContext,
) -> Response[Union[CreateCustomFieldContext, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: CreateCustomFieldContext,
) -> Optional[Union[CreateCustomFieldContext, None, None, None, None]]:
    """Creates a custom field context.

    If `projectIds` is empty, a global context is created. A global context is one that applies to all project. If `issueTypeIds` is empty, the context applies to all issue types.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            field_id=field_id,
            json_body=json_body,
        )
    ).parsed
