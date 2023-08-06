from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.issue_update_details import IssueUpdateDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "notifyUsers": notify_users,
        "overrideScreenSecurity": override_screen_security,
        "overrideEditableFlag": override_editable_flag,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
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
    issue_id_or_key: str,
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[None, None, None, None, None]]:
    """Edits an issue. A transition may be applied and issue properties updated as part of the edit.

    The edits to the issue's fields are defined using `update` and `fields`. The fields that can be edited are determined using [ Get edit issue metadata](#api-rest-api-3-issue-issueIdOrKey-editmeta-get).

    The parent field may be set by key or ID. For standard issue types, the parent may be removed by setting `update.parent.set.none` to *true*. Note that the `description`, `environment`, and any `textarea` type custom fields (multi-line text fields) take Atlassian Document Format content. Single line custom fields (`textfield`) accept a string and don't handle Atlassian Document Format content.

    Connect app users with admin permissions (from user permissions and app scopes) can override the screen security configuration using `overrideScreenSecurity` and `overrideEditableFlag`.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Edit issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[None, None, None, None, None]]:
    """Edits an issue. A transition may be applied and issue properties updated as part of the edit.

    The edits to the issue's fields are defined using `update` and `fields`. The fields that can be edited are determined using [ Get edit issue metadata](#api-rest-api-3-issue-issueIdOrKey-editmeta-get).

    The parent field may be set by key or ID. For standard issue types, the parent may be removed by setting `update.parent.set.none` to *true*. Note that the `description`, `environment`, and any `textarea` type custom fields (multi-line text fields) take Atlassian Document Format content. Single line custom fields (`textfield`) accept a string and don't handle Atlassian Document Format content.

    Connect app users with admin permissions (from user permissions and app scopes) can override the screen security configuration using `overrideScreenSecurity` and `overrideEditableFlag`.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Edit issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            json_body=json_body,
            notify_users=notify_users,
            override_screen_security=override_screen_security,
            override_editable_flag=override_editable_flag,
        )
    ).parsed
