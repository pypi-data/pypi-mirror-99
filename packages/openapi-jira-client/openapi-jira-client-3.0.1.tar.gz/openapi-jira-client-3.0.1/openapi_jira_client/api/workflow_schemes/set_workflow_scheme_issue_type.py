from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.issue_type_workflow_mapping import IssueTypeWorkflowMapping
from ...models.workflow_scheme import WorkflowScheme
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflowscheme/{id}/issuetype/{issueType}".format(
        client.base_url, id=id_, issueType=issue_type
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[WorkflowScheme, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = WorkflowScheme.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[WorkflowScheme, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Response[Union[WorkflowScheme, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        issue_type=issue_type,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Optional[Union[WorkflowScheme, None, None, None, None]]:
    """Sets the workflow for an issue type in a workflow scheme.

    Note that active workflow schemes cannot be edited. If the workflow scheme is active, set `updateDraftIfNeeded` to `true` in the request body and a draft workflow scheme is created or updated with the new issue type-workflow mapping. The draft workflow scheme can be published in Jira.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id_=id_,
        issue_type=issue_type,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Response[Union[WorkflowScheme, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        issue_type=issue_type,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Optional[Union[WorkflowScheme, None, None, None, None]]:
    """Sets the workflow for an issue type in a workflow scheme.

    Note that active workflow schemes cannot be edited. If the workflow scheme is active, set `updateDraftIfNeeded` to `true` in the request body and a draft workflow scheme is created or updated with the new issue type-workflow mapping. The draft workflow scheme can be published in Jira.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            issue_type=issue_type,
            json_body=json_body,
        )
    ).parsed
