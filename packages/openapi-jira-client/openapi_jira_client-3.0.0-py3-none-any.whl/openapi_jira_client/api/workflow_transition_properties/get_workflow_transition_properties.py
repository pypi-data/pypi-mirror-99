from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.get_workflow_transition_properties_workflow_mode import GetWorkflowTransitionPropertiesWorkflowMode
from ...models.workflow_transition_property import WorkflowTransitionProperty
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    transition_id: int,
    include_reserved_keys: Union[Unset, bool] = False,
    key: Union[Unset, str] = UNSET,
    workflow_name: str,
    workflow_mode: Union[
        Unset, GetWorkflowTransitionPropertiesWorkflowMode
    ] = GetWorkflowTransitionPropertiesWorkflowMode.LIVE,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflow/transitions/{transitionId}/properties".format(
        client.base_url, transitionId=transition_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_workflow_mode: Union[Unset, GetWorkflowTransitionPropertiesWorkflowMode] = UNSET
    if not isinstance(workflow_mode, Unset):
        json_workflow_mode = workflow_mode

    params: Dict[str, Any] = {
        "includeReservedKeys": include_reserved_keys,
        "key": key,
        "workflowName": workflow_name,
        "workflowMode": json_workflow_mode,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[WorkflowTransitionProperty, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = WorkflowTransitionProperty.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[WorkflowTransitionProperty, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    transition_id: int,
    include_reserved_keys: Union[Unset, bool] = False,
    key: Union[Unset, str] = UNSET,
    workflow_name: str,
    workflow_mode: Union[
        Unset, GetWorkflowTransitionPropertiesWorkflowMode
    ] = GetWorkflowTransitionPropertiesWorkflowMode.LIVE,
) -> Response[Union[WorkflowTransitionProperty, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        transition_id=transition_id,
        include_reserved_keys=include_reserved_keys,
        key=key,
        workflow_name=workflow_name,
        workflow_mode=workflow_mode,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    transition_id: int,
    include_reserved_keys: Union[Unset, bool] = False,
    key: Union[Unset, str] = UNSET,
    workflow_name: str,
    workflow_mode: Union[
        Unset, GetWorkflowTransitionPropertiesWorkflowMode
    ] = GetWorkflowTransitionPropertiesWorkflowMode.LIVE,
) -> Optional[Union[WorkflowTransitionProperty, None, None, None, None]]:
    """Returns the properties on a workflow transition. Transition properties are used to change the behavior of a transition. For more information, see [Transition properties](https://confluence.atlassian.com/x/zIhKLg#Advancedworkflowconfiguration-transitionproperties) and [Workflow properties](https://confluence.atlassian.com/x/JYlKLg).

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        transition_id=transition_id,
        include_reserved_keys=include_reserved_keys,
        key=key,
        workflow_name=workflow_name,
        workflow_mode=workflow_mode,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    transition_id: int,
    include_reserved_keys: Union[Unset, bool] = False,
    key: Union[Unset, str] = UNSET,
    workflow_name: str,
    workflow_mode: Union[
        Unset, GetWorkflowTransitionPropertiesWorkflowMode
    ] = GetWorkflowTransitionPropertiesWorkflowMode.LIVE,
) -> Response[Union[WorkflowTransitionProperty, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        transition_id=transition_id,
        include_reserved_keys=include_reserved_keys,
        key=key,
        workflow_name=workflow_name,
        workflow_mode=workflow_mode,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    transition_id: int,
    include_reserved_keys: Union[Unset, bool] = False,
    key: Union[Unset, str] = UNSET,
    workflow_name: str,
    workflow_mode: Union[
        Unset, GetWorkflowTransitionPropertiesWorkflowMode
    ] = GetWorkflowTransitionPropertiesWorkflowMode.LIVE,
) -> Optional[Union[WorkflowTransitionProperty, None, None, None, None]]:
    """Returns the properties on a workflow transition. Transition properties are used to change the behavior of a transition. For more information, see [Transition properties](https://confluence.atlassian.com/x/zIhKLg#Advancedworkflowconfiguration-transitionproperties) and [Workflow properties](https://confluence.atlassian.com/x/JYlKLg).

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            transition_id=transition_id,
            include_reserved_keys=include_reserved_keys,
            key=key,
            workflow_name=workflow_name,
            workflow_mode=workflow_mode,
        )
    ).parsed
