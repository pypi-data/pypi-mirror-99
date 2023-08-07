from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_top_chunk_out import ExtractTopChunkOut
from ...models.http_validation_error import HTTPValidationError
from ...models.synchronous_extract_create import SynchronousExtractCreate
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: SynchronousExtractCreate,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/tasks/synchronous/".format(client.base_url)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[List[ExtractTopChunkOut], None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExtractTopChunkOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[List[ExtractTopChunkOut], None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SynchronousExtractCreate,
) -> Response[Union[List[ExtractTopChunkOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: SynchronousExtractCreate,
) -> Optional[Union[List[ExtractTopChunkOut], None, None, HTTPValidationError]]:
    """Create and run a synchronous extract task.

    Only orgadmins are allowed to run synchronous extract tasks.
    The id of the organization is inferred from the session token.

    If model id is passed in the parameters, the task is created from the models.
    Otherwise, the seeds or the config to base the extract on must be passed in the body."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SynchronousExtractCreate,
) -> Response[Union[List[ExtractTopChunkOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: SynchronousExtractCreate,
) -> Optional[Union[List[ExtractTopChunkOut], None, None, HTTPValidationError]]:
    """Create and run a synchronous extract task.

    Only orgadmins are allowed to run synchronous extract tasks.
    The id of the organization is inferred from the session token.

    If model id is passed in the parameters, the task is created from the models.
    Otherwise, the seeds or the config to base the extract on must be passed in the body."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
