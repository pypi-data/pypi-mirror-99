from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...models.attachment import Attachment
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/attachments".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[Attachment], None, None, None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Attachment.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 413:
        response_413 = None

        return response_413
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[Attachment], None, None, None]]:
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
) -> Response[Union[List[Attachment], None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Optional[Union[List[Attachment], None, None, None]]:
    """Adds one or more attachments to an issue. Attachments are posted as multipart/form-data ([RFC 1867](https://www.ietf.org/rfc/rfc1867.txt)).

    Note that:

     *  The request must have a `X-Atlassian-Token: no-check` header, if not it is blocked. See [Special headers](#special-request-headers) for more information.
     *  The name of the multipart/form-data parameter that contains the attachments must be `file`.

    The following example uploads a file called *myfile.txt* to the issue *TEST-123*:

    `curl -D- -u admin:admin -X POST -H \"X-Atlassian-Token: no-check\" -F \"file=@myfile.txt\" https://your-domain.atlassian.net/rest/api/3/issue/TEST-123/attachments`

    Tip: Use a client library. Many client libraries have classes for handling multipart POST operations. For example, in Java, the Apache HTTP Components library provides a [MultiPartEntity](http://hc.apache.org/httpcomponents-client-ga/httpmime/apidocs/org/apache/http/entity/mime/MultipartEntity.html) class for multipart POST operations.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse Projects* and *Create attachments* [ project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Response[Union[List[Attachment], None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Optional[Union[List[Attachment], None, None, None]]:
    """Adds one or more attachments to an issue. Attachments are posted as multipart/form-data ([RFC 1867](https://www.ietf.org/rfc/rfc1867.txt)).

    Note that:

     *  The request must have a `X-Atlassian-Token: no-check` header, if not it is blocked. See [Special headers](#special-request-headers) for more information.
     *  The name of the multipart/form-data parameter that contains the attachments must be `file`.

    The following example uploads a file called *myfile.txt* to the issue *TEST-123*:

    `curl -D- -u admin:admin -X POST -H \"X-Atlassian-Token: no-check\" -F \"file=@myfile.txt\" https://your-domain.atlassian.net/rest/api/3/issue/TEST-123/attachments`

    Tip: Use a client library. Many client libraries have classes for handling multipart POST operations. For example, in Java, the Apache HTTP Components library provides a [MultiPartEntity](http://hc.apache.org/httpcomponents-client-ga/httpmime/apidocs/org/apache/http/entity/mime/MultipartEntity.html) class for multipart POST operations.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse Projects* and *Create attachments* [ project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
        )
    ).parsed
