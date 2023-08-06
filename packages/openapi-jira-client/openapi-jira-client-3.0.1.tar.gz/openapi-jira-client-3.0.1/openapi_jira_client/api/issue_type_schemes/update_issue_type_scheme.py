from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.issue_type_scheme_update_details import IssueTypeSchemeUpdateDetails
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_type_scheme_id: int,
    json_body: IssueTypeSchemeUpdateDetails,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issuetypescheme/{issueTypeSchemeId}".format(
        client.base_url, issueTypeSchemeId=issue_type_scheme_id
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
    issue_type_scheme_id: int,
    json_body: IssueTypeSchemeUpdateDetails,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_type_scheme_id=issue_type_scheme_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_type_scheme_id: int,
    json_body: IssueTypeSchemeUpdateDetails,
) -> Optional[Union[None, None, None, None, None]]:
    """Updates an issue type scheme.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        issue_type_scheme_id=issue_type_scheme_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_type_scheme_id: int,
    json_body: IssueTypeSchemeUpdateDetails,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_type_scheme_id=issue_type_scheme_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_type_scheme_id: int,
    json_body: IssueTypeSchemeUpdateDetails,
) -> Optional[Union[None, None, None, None, None]]:
    """Updates an issue type scheme.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            issue_type_scheme_id=issue_type_scheme_id,
            json_body=json_body,
        )
    ).parsed
