from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.error_collection import ErrorCollection
from ...models.get_fields_paginated_order_by import GetFieldsPaginatedOrderBy
from ...models.get_fields_paginated_type_item import GetFieldsPaginatedTypeItem
from ...models.page_bean_field import PageBeanField
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    type: Union[Unset, List[GetFieldsPaginatedTypeItem]] = UNSET,
    id: Union[Unset, List[str]] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetFieldsPaginatedOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_type: Union[Unset, List[Any]] = UNSET
    if not isinstance(type, Unset):
        json_type = []
        for type_item_data in type:
            type_item = type_item_data.value

            json_type.append(type_item)

    json_id: Union[Unset, List[Any]] = UNSET
    if not isinstance(id, Unset):
        json_id = id

    json_order_by: Union[Unset, GetFieldsPaginatedOrderBy] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "type": json_type,
        "id": json_id,
        "query": query,
        "orderBy": json_order_by,
        "expand": expand,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[PageBeanField, ErrorCollection, None, ErrorCollection]]:
    if response.status_code == 200:
        response_200 = PageBeanField.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[PageBeanField, ErrorCollection, None, ErrorCollection]]:
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
    type: Union[Unset, List[GetFieldsPaginatedTypeItem]] = UNSET,
    id: Union[Unset, List[str]] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetFieldsPaginatedOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[PageBeanField, ErrorCollection, None, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        type=type,
        id=id,
        query=query,
        order_by=order_by,
        expand=expand,
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
    type: Union[Unset, List[GetFieldsPaginatedTypeItem]] = UNSET,
    id: Union[Unset, List[str]] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetFieldsPaginatedOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[PageBeanField, ErrorCollection, None, ErrorCollection]]:
    """Returns a [paginated](#pagination) list of fields for Classic Jira projects. The list can include:

     *  all fields.
     *  specific fields, by defining `id`.
     *  fields that contain a string in the field name or description, by defining `query`.
     *  specific fields that contain a string in the field name or description, by defining `id` and `query`.

    Only custom fields can be queried, `type` must be set to `custom`.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        type=type,
        id=id,
        query=query,
        order_by=order_by,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    type: Union[Unset, List[GetFieldsPaginatedTypeItem]] = UNSET,
    id: Union[Unset, List[str]] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetFieldsPaginatedOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[PageBeanField, ErrorCollection, None, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        type=type,
        id=id,
        query=query,
        order_by=order_by,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    type: Union[Unset, List[GetFieldsPaginatedTypeItem]] = UNSET,
    id: Union[Unset, List[str]] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetFieldsPaginatedOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[PageBeanField, ErrorCollection, None, ErrorCollection]]:
    """Returns a [paginated](#pagination) list of fields for Classic Jira projects. The list can include:

     *  all fields.
     *  specific fields, by defining `id`.
     *  fields that contain a string in the field name or description, by defining `query`.
     *  specific fields that contain a string in the field name or description, by defining `id` and `query`.

    Only custom fields can be queried, `type` must be set to `custom`.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            type=type,
            id=id,
            query=query,
            order_by=order_by,
            expand=expand,
        )
    ).parsed
