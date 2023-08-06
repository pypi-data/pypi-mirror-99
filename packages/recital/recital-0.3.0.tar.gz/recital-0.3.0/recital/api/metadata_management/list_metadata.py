from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.metadata_out import MetadataOut
from ...models.metadata_source import MetadataSource
from ...models.metadata_type import MetadataType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
    name: Union[Unset, str] = UNSET,
    source: Union[Unset, MetadataSource] = UNSET,
    value_type: Union[Unset, MetadataType] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_source: Union[Unset, MetadataSource] = UNSET
    if not isinstance(source, Unset):
        json_source = source

    json_value_type: Union[Unset, MetadataType] = UNSET
    if not isinstance(value_type, Unset):
        json_value_type = value_type

    params: Dict[str, Any] = {
        "org_id": org_id,
        "limit": limit,
        "offset": offset,
        "name": name,
        "source": json_source,
        "value_type": json_value_type,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[MetadataOut], None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MetadataOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[MetadataOut], None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
    name: Union[Unset, str] = UNSET,
    source: Union[Unset, MetadataSource] = UNSET,
    value_type: Union[Unset, MetadataType] = UNSET,
) -> Response[Union[List[MetadataOut], None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        org_id=org_id,
        limit=limit,
        offset=offset,
        name=name,
        source=source,
        value_type=value_type,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
    name: Union[Unset, str] = UNSET,
    source: Union[Unset, MetadataSource] = UNSET,
    value_type: Union[Unset, MetadataType] = UNSET,
) -> Optional[Union[List[MetadataOut], None, HTTPValidationError]]:
    """List organization's metadata.

    Only basic users, orgadmins and services can have access to metadata.
    * If the user is a user, the id of the organization is guessed from the session token.
    * If the user is a service, the org_id query parameter is expected

    For users:
    * If filter is passed, the route only returns the metadata matching the filter.
    (e.g., filter=si will return size).
    * If type is specified, the route only returns the metadata of this type.
    * If source is specified, the route only returns the metadata from this source."""

    return sync_detailed(
        client=client,
        org_id=org_id,
        limit=limit,
        offset=offset,
        name=name,
        source=source,
        value_type=value_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
    name: Union[Unset, str] = UNSET,
    source: Union[Unset, MetadataSource] = UNSET,
    value_type: Union[Unset, MetadataType] = UNSET,
) -> Response[Union[List[MetadataOut], None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        org_id=org_id,
        limit=limit,
        offset=offset,
        name=name,
        source=source,
        value_type=value_type,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
    name: Union[Unset, str] = UNSET,
    source: Union[Unset, MetadataSource] = UNSET,
    value_type: Union[Unset, MetadataType] = UNSET,
) -> Optional[Union[List[MetadataOut], None, HTTPValidationError]]:
    """List organization's metadata.

    Only basic users, orgadmins and services can have access to metadata.
    * If the user is a user, the id of the organization is guessed from the session token.
    * If the user is a service, the org_id query parameter is expected

    For users:
    * If filter is passed, the route only returns the metadata matching the filter.
    (e.g., filter=si will return size).
    * If type is specified, the route only returns the metadata of this type.
    * If source is specified, the route only returns the metadata from this source."""

    return (
        await asyncio_detailed(
            client=client,
            org_id=org_id,
            limit=limit,
            offset=offset,
            name=name,
            source=source,
            value_type=value_type,
        )
    ).parsed
