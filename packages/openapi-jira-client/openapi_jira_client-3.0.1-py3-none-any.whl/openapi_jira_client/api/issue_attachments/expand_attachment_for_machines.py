from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.attachment_archive_impl import AttachmentArchiveImpl
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/attachment/{id}/expand/raw".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AttachmentArchiveImpl, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = AttachmentArchiveImpl.from_dict(response.json())

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
    if response.status_code == 409:
        response_409 = None

        return response_409
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AttachmentArchiveImpl, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Response[Union[AttachmentArchiveImpl, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Optional[Union[AttachmentArchiveImpl, None, None, None, None]]:
    """Returns the metadata for the contents of an attachment, if it is an archive. For example, if the attachment is a ZIP archive, then information about the files in the archive is returned. Currently, only the ZIP archive format is supported.

    Use this operation if you are processing the data without presenting it to the user, as this operation only returns the metadata for the contents of the attachment. Otherwise, to retrieve data to present to the user, use [ Get all metadata for an expanded attachment](#api-rest-api-3-attachment-id-expand-human-get) which also returns the metadata for the attachment itself, such as the attachment's ID and name.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** For the issue containing the attachment:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        id_=id_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Response[Union[AttachmentArchiveImpl, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: str,
) -> Optional[Union[AttachmentArchiveImpl, None, None, None, None]]:
    """Returns the metadata for the contents of an attachment, if it is an archive. For example, if the attachment is a ZIP archive, then information about the files in the archive is returned. Currently, only the ZIP archive format is supported.

    Use this operation if you are processing the data without presenting it to the user, as this operation only returns the metadata for the contents of the attachment. Otherwise, to retrieve data to present to the user, use [ Get all metadata for an expanded attachment](#api-rest-api-3-attachment-id-expand-human-get) which also returns the metadata for the attachment itself, such as the attachment's ID and name.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** For the issue containing the attachment:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
        )
    ).parsed
