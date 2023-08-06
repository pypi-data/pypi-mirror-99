from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.delete_worklog_adjust_estimate import DeleteWorklogAdjustEstimate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/worklog/{id}".format(
        client.base_url, issueIdOrKey=issue_id_or_key, id=id_
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_adjust_estimate: Union[Unset, str] = UNSET
    if not isinstance(adjust_estimate, Unset):
        json_adjust_estimate = adjust_estimate.value

    params: Dict[str, Any] = {
        "notifyUsers": notify_users,
        "adjustEstimate": json_adjust_estimate,
        "newEstimate": new_estimate,
        "increaseBy": increase_by,
        "overrideEditableFlag": override_editable_flag,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None]]:
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
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        increase_by=increase_by,
        override_editable_flag=override_editable_flag,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[None, None, None, None]]:
    """Deletes a worklog from an issue.

    Time tracking must be enabled in Jira, otherwise this operation returns an error. For more information, see [Configuring time tracking](https://confluence.atlassian.com/x/qoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Delete all worklogs*[ project permission](https://confluence.atlassian.com/x/yodKLg) to delete any worklog or *Delete own worklogs* to delete worklogs created by the user,
     *  If the worklog has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        increase_by=increase_by,
        override_editable_flag=override_editable_flag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        increase_by=increase_by,
        override_editable_flag=override_editable_flag,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[None, None, None, None]]:
    """Deletes a worklog from an issue.

    Time tracking must be enabled in Jira, otherwise this operation returns an error. For more information, see [Configuring time tracking](https://confluence.atlassian.com/x/qoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Delete all worklogs*[ project permission](https://confluence.atlassian.com/x/yodKLg) to delete any worklog or *Delete own worklogs* to delete worklogs created by the user,
     *  If the worklog has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            id_=id_,
            notify_users=notify_users,
            adjust_estimate=adjust_estimate,
            new_estimate=new_estimate,
            increase_by=increase_by,
            override_editable_flag=override_editable_flag,
        )
    ).parsed
