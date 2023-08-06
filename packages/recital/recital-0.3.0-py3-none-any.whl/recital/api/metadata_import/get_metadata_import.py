from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.metadata_import_out import MetadataImportOut
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/import/{metadata_import_id}/".format(
        client.base_url, metadata_import_id=metadata_import_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[MetadataImportOut, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = MetadataImportOut.from_dict(response.json())

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
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[MetadataImportOut, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
) -> Response[Union[MetadataImportOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_import_id=metadata_import_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
) -> Optional[Union[MetadataImportOut, None, None, None, HTTPValidationError]]:
    """Get a pending or executing metadata import tasks.

    Only orgadmins and services can access metadata import tasks."""

    return sync_detailed(
        client=client,
        metadata_import_id=metadata_import_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
) -> Response[Union[MetadataImportOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_import_id=metadata_import_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
) -> Optional[Union[MetadataImportOut, None, None, None, HTTPValidationError]]:
    """Get a pending or executing metadata import tasks.

    Only orgadmins and services can access metadata import tasks."""

    return (
        await asyncio_detailed(
            client=client,
            metadata_import_id=metadata_import_id,
        )
    ).parsed
