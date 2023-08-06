from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
    json_body: None,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}".format(
        client.base_url, dashboardId=dashboard_id, itemId=item_id, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = None

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 201:
        response_201 = None

        return response_201
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
    dashboard_id: str,
    item_id: str,
    property_key: str,
    json_body: None,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
        property_key=property_key,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
    json_body: None,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Sets the value of a dashboard item property. Use this resource in apps to store custom data against a dashboard item.

    A dashboard item enables an app to add user-specific information to a user dashboard. Dashboard items are exposed to users as gadgets that users can add to their dashboards. For more information on how users do this, see [Adding and customizing gadgets](https://confluence.atlassian.com/x/7AeiLQ).

    When an app creates a dashboard item it registers a callback to receive the dashboard item ID. The callback fires whenever the item is rendered or, where the item is configurable, the user edits the item. The app then uses this resource to store the item's content or configuration details. For more information on working with dashboard items, see [ Building a dashboard item for a JIRA Connect add-on](https://developer.atlassian.com/server/jira/platform/guide-building-a-dashboard-item-for-a-jira-connect-add-on-33746254/) and the [Dashboard Item](https://developer.atlassian.com/cloud/jira/platform/modules/dashboard-item/) documentation.

    There is no resource to set or get dashboard items.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The user must be the owner of the dashboard. Note, users with the *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) are considered owners of the System dashboard."""

    return sync_detailed(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
        property_key=property_key,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
    json_body: None,
) -> Response[Union[None, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
        property_key=property_key,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
    property_key: str,
    json_body: None,
) -> Optional[Union[None, None, None, None, None, None]]:
    """Sets the value of a dashboard item property. Use this resource in apps to store custom data against a dashboard item.

    A dashboard item enables an app to add user-specific information to a user dashboard. Dashboard items are exposed to users as gadgets that users can add to their dashboards. For more information on how users do this, see [Adding and customizing gadgets](https://confluence.atlassian.com/x/7AeiLQ).

    When an app creates a dashboard item it registers a callback to receive the dashboard item ID. The callback fires whenever the item is rendered or, where the item is configurable, the user edits the item. The app then uses this resource to store the item's content or configuration details. For more information on working with dashboard items, see [ Building a dashboard item for a JIRA Connect add-on](https://developer.atlassian.com/server/jira/platform/guide-building-a-dashboard-item-for-a-jira-connect-add-on-33746254/) and the [Dashboard Item](https://developer.atlassian.com/cloud/jira/platform/modules/dashboard-item/) documentation.

    There is no resource to set or get dashboard items.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The user must be the owner of the dashboard. Note, users with the *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) are considered owners of the System dashboard."""

    return (
        await asyncio_detailed(
            client=client,
            dashboard_id=dashboard_id,
            item_id=item_id,
            property_key=property_key,
            json_body=json_body,
        )
    ).parsed
