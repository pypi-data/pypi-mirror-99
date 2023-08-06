from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.delete_issue_delete_subtasks import DeleteIssueDeleteSubtasks
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_delete_subtasks: Union[Unset, str] = UNSET
    if not isinstance(delete_subtasks, Unset):
        json_delete_subtasks = delete_subtasks.value

    params: Dict[str, Any] = {
        "deleteSubtasks": json_delete_subtasks,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        delete_subtasks=delete_subtasks,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes an issue.

    An issue cannot be deleted if it has one or more subtasks. To delete an issue with subtasks, set `deleteSubtasks`. This causes the issue's subtasks to be deleted with the issue.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Delete issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the issue.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        delete_subtasks=delete_subtasks,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        delete_subtasks=delete_subtasks,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Optional[Union[None, None, None, None, None]]:
    """Deletes an issue.

    An issue cannot be deleted if it has one or more subtasks. To delete an issue with subtasks, set `deleteSubtasks`. This causes the issue's subtasks to be deleted with the issue.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Delete issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the issue.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            delete_subtasks=delete_subtasks,
        )
    ).parsed
