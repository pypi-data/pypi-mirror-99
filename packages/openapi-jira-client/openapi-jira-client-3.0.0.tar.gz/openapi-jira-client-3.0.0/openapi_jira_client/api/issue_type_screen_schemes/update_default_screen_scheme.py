from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.update_default_screen_scheme import UpdateDefaultScreenScheme
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_type_screen_scheme_id: str,
    json_body: UpdateDefaultScreenScheme,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/default".format(
        client.base_url, issueTypeScreenSchemeId=issue_type_screen_scheme_id
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
    issue_type_screen_scheme_id: str,
    json_body: UpdateDefaultScreenScheme,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_type_screen_scheme_id=issue_type_screen_scheme_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_type_screen_scheme_id: str,
    json_body: UpdateDefaultScreenScheme,
) -> Optional[Union[None, None, None, None, None]]:
    """Updates the default screen scheme of an issue type screen scheme. The default screen scheme is used for all unmapped issue types.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        issue_type_screen_scheme_id=issue_type_screen_scheme_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_type_screen_scheme_id: str,
    json_body: UpdateDefaultScreenScheme,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_type_screen_scheme_id=issue_type_screen_scheme_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_type_screen_scheme_id: str,
    json_body: UpdateDefaultScreenScheme,
) -> Optional[Union[None, None, None, None, None]]:
    """Updates the default screen scheme of an issue type screen scheme. The default screen scheme is used for all unmapped issue types.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            issue_type_screen_scheme_id=issue_type_screen_scheme_id,
            json_body=json_body,
        )
    ).parsed
