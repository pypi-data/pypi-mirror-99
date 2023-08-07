from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.metadata_create import MetadataCreate
from ...models.metadata_out import MetadataOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: MetadataCreate,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    org_id: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "folder_id": folder_id,
        "version_id": version_id,
        "org_id": org_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[MetadataOut, None, None, None, None, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = MetadataOut.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 409:
        response_409 = None

        return response_409
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
) -> Response[Union[MetadataOut, None, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: MetadataCreate,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    org_id: Union[Unset, int] = UNSET,
) -> Response[Union[MetadataOut, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        org_id=org_id,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: MetadataCreate,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    org_id: Union[Unset, int] = UNSET,
) -> Optional[Union[MetadataOut, None, None, None, None, HTTPValidationError]]:
    """Create a metadata and set its value to documents or folders.

    Only orgadmins and services can create metadata.

    If a service makes the query, the org_id parameter is expected,
    and the metadata is only created, no value is assigned to folders or versions.
    For this reason, in this case a value is not expected, but value_type is required.

    For orgadmins, the organization id is inferred from the session token, and:
    - If the version parameter is passed, the specified value is assigned to the version.
    - If the folder parameter is passed, the specified value is assigned to all of the
    documents in the folder and its children.
    - If neither is passed, the value is assigned to all documents in the organization.

    In any case, the metadata is created if it doesn't already exist.
    The metadata source is automatically set to user."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        org_id=org_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: MetadataCreate,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    org_id: Union[Unset, int] = UNSET,
) -> Response[Union[MetadataOut, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        org_id=org_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: MetadataCreate,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    org_id: Union[Unset, int] = UNSET,
) -> Optional[Union[MetadataOut, None, None, None, None, HTTPValidationError]]:
    """Create a metadata and set its value to documents or folders.

    Only orgadmins and services can create metadata.

    If a service makes the query, the org_id parameter is expected,
    and the metadata is only created, no value is assigned to folders or versions.
    For this reason, in this case a value is not expected, but value_type is required.

    For orgadmins, the organization id is inferred from the session token, and:
    - If the version parameter is passed, the specified value is assigned to the version.
    - If the folder parameter is passed, the specified value is assigned to all of the
    documents in the folder and its children.
    - If neither is passed, the value is assigned to all documents in the organization.

    In any case, the metadata is created if it doesn't already exist.
    The metadata source is automatically set to user."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            folder_id=folder_id,
            version_id=version_id,
            org_id=org_id,
        )
    ).parsed
