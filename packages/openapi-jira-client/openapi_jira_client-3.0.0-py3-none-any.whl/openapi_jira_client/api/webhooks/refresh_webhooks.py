from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.container_for_webhook_i_ds import ContainerForWebhookIDs
from ...models.error_collection import ErrorCollection
from ...models.webhooks_expiration_date import WebhooksExpirationDate
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: ContainerForWebhookIDs,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/webhook/refresh".format(client.base_url)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[WebhooksExpirationDate, ErrorCollection, ErrorCollection]]:
    if response.status_code == 200:
        response_200 = WebhooksExpirationDate.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[WebhooksExpirationDate, ErrorCollection, ErrorCollection]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ContainerForWebhookIDs,
) -> Response[Union[WebhooksExpirationDate, ErrorCollection, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: ContainerForWebhookIDs,
) -> Optional[Union[WebhooksExpirationDate, ErrorCollection, ErrorCollection]]:
    """Webhooks registered through the REST API expire after 30 days. Call this resource periodically to keep them alive.

    Unrecognized webhook IDs (nonexistent or belonging to other apps) are ignored.

    **[Permissions](#permissions) required:** Only [Connect apps](https://developer.atlassian.com/cloud/jira/platform/integrating-with-jira-cloud/#atlassian-connect) can use this operation."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ContainerForWebhookIDs,
) -> Response[Union[WebhooksExpirationDate, ErrorCollection, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: ContainerForWebhookIDs,
) -> Optional[Union[WebhooksExpirationDate, ErrorCollection, ErrorCollection]]:
    """Webhooks registered through the REST API expire after 30 days. Call this resource periodically to keep them alive.

    Unrecognized webhook IDs (nonexistent or belonging to other apps) are ignored.

    **[Permissions](#permissions) required:** Only [Connect apps](https://developer.atlassian.com/cloud/jira/platform/integrating-with-jira-cloud/#atlassian-connect) can use this operation."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
