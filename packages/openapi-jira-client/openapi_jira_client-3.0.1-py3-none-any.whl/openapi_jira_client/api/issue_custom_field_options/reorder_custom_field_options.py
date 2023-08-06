from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.order_of_custom_field_options import OrderOfCustomFieldOptions
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: OrderOfCustomFieldOptions,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context/{contextId}/option/move".format(
        client.base_url, fieldId=field_id, contextId=context_id
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
    field_id: str,
    context_id: int,
    json_body: OrderOfCustomFieldOptions,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: OrderOfCustomFieldOptions,
) -> Optional[Union[None, None, None, None, None]]:
    """Changes the order of custom field options or cascading options in a context.

    This operation works for custom field options created in Jira or the operations from this resource. **To work with issue field select list options created for Connect apps use the [Issue custom field options (apps)](#api-group-issue-custom-field-options--apps-) operations.**

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        field_id=field_id,
        context_id=context_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: OrderOfCustomFieldOptions,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: OrderOfCustomFieldOptions,
) -> Optional[Union[None, None, None, None, None]]:
    """Changes the order of custom field options or cascading options in a context.

    This operation works for custom field options created in Jira or the operations from this resource. **To work with issue field select list options created for Connect apps use the [Issue custom field options (apps)](#api-group-issue-custom-field-options--apps-) operations.**

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            field_id=field_id,
            context_id=context_id,
            json_body=json_body,
        )
    ).parsed
