from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.issue_types_workflow_mapping import IssueTypesWorkflowMapping
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id: int,
    workflow_name: Union[Unset, str] = UNSET,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflowscheme/{id}/workflow".format(client.base_url, id=id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "workflowName": workflow_name,
        "returnDraftIfExists": return_draft_if_exists,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueTypesWorkflowMapping, None, None, None]]:
    if response.status_code == 200:
        response_200 = IssueTypesWorkflowMapping.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[IssueTypesWorkflowMapping, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id: int,
    workflow_name: Union[Unset, str] = UNSET,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Response[Union[IssueTypesWorkflowMapping, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        workflow_name=workflow_name,
        return_draft_if_exists=return_draft_if_exists,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id: int,
    workflow_name: Union[Unset, str] = UNSET,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Optional[Union[IssueTypesWorkflowMapping, None, None, None]]:
    """Returns the workflow-issue type mappings for a workflow scheme.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id=id,
        workflow_name=workflow_name,
        return_draft_if_exists=return_draft_if_exists,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id: int,
    workflow_name: Union[Unset, str] = UNSET,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Response[Union[IssueTypesWorkflowMapping, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        workflow_name=workflow_name,
        return_draft_if_exists=return_draft_if_exists,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id: int,
    workflow_name: Union[Unset, str] = UNSET,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Optional[Union[IssueTypesWorkflowMapping, None, None, None]]:
    """Returns the workflow-issue type mappings for a workflow scheme.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            workflow_name=workflow_name,
            return_draft_if_exists=return_draft_if_exists,
        )
    ).parsed
