from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.page_bean_notification_scheme import PageBeanNotificationScheme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/notificationscheme".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[PageBeanNotificationScheme, None]]:
    if response.status_code == 200:
        response_200 = PageBeanNotificationScheme.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PageBeanNotificationScheme, None]]:
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
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[PageBeanNotificationScheme, None]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
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
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[PageBeanNotificationScheme, None]]:
    """Returns a [paginated](#pagination) list of [notification schemes](https://confluence.atlassian.com/x/8YdKLg) ordered by display name.

    ### About notification schemes ###

    A notification scheme is a list of events and recipients who will receive notifications for those events. The list is contained within the `notificationSchemeEvents` object and contains pairs of `events` and `notifications`:

     *  `event` Identifies the type of event. The events can be [Jira system events](https://confluence.atlassian.com/x/8YdKLg#Creatinganotificationscheme-eventsEvents) or [custom events](https://confluence.atlassian.com/x/AIlKLg).
     *  `notifications` Identifies the [recipients](https://confluence.atlassian.com/x/8YdKLg#Creatinganotificationscheme-recipientsRecipients) of notifications for each event. Recipients can be any of the following types:

         *  `CurrentAssignee`
         *  `Reporter`
         *  `CurrentUser`
         *  `ProjectLead`
         *  `ComponentLead`
         *  `User` (the `parameter` is the user key)
         *  `Group` (the `parameter` is the group name)
         *  `ProjectRole` (the `parameter` is the project role ID)
         *  `EmailAddress`
         *  `AllWatchers`
         *  `UserCustomField` (the `parameter` is the ID of the custom field)
         *  `GroupCustomField`(the `parameter` is the ID of the custom field)

    *Note that you should allow for events without recipients to appear in responses.*

    **[Permissions](#permissions) required:** Permission to access Jira, however the user must have permission to administer at least one project associated with a notification scheme for it to be returned."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[PageBeanNotificationScheme, None]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
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
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[PageBeanNotificationScheme, None]]:
    """Returns a [paginated](#pagination) list of [notification schemes](https://confluence.atlassian.com/x/8YdKLg) ordered by display name.

    ### About notification schemes ###

    A notification scheme is a list of events and recipients who will receive notifications for those events. The list is contained within the `notificationSchemeEvents` object and contains pairs of `events` and `notifications`:

     *  `event` Identifies the type of event. The events can be [Jira system events](https://confluence.atlassian.com/x/8YdKLg#Creatinganotificationscheme-eventsEvents) or [custom events](https://confluence.atlassian.com/x/AIlKLg).
     *  `notifications` Identifies the [recipients](https://confluence.atlassian.com/x/8YdKLg#Creatinganotificationscheme-recipientsRecipients) of notifications for each event. Recipients can be any of the following types:

         *  `CurrentAssignee`
         *  `Reporter`
         *  `CurrentUser`
         *  `ProjectLead`
         *  `ComponentLead`
         *  `User` (the `parameter` is the user key)
         *  `Group` (the `parameter` is the group name)
         *  `ProjectRole` (the `parameter` is the project role ID)
         *  `EmailAddress`
         *  `AllWatchers`
         *  `UserCustomField` (the `parameter` is the ID of the custom field)
         *  `GroupCustomField`(the `parameter` is the ID of the custom field)

    *Note that you should allow for events without recipients to appear in responses.*

    **[Permissions](#permissions) required:** Permission to access Jira, however the user must have permission to administer at least one project associated with a notification scheme for it to be returned."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            expand=expand,
        )
    ).parsed
