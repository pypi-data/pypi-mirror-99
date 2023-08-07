from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.chunk_result import ChunkResult
from ..models.search_result_pipeline_logs import SearchResultPipelineLogs
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResultChunks")


@attr.s(auto_attribs=True)
class SearchResultChunks:
    """ Schema for search result chunks. """

    query_id: int
    chunks: List[ChunkResult]
    stripped_query: List[str]
    pipeline_logs: Union[SearchResultPipelineLogs, Unset] = UNSET
    suggested_query: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_id = self.query_id
        chunks = []
        for chunks_item_data in self.chunks:
            chunks_item = chunks_item_data.to_dict()

            chunks.append(chunks_item)

        stripped_query = self.stripped_query

        pipeline_logs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pipeline_logs, Unset):
            pipeline_logs = self.pipeline_logs.to_dict()

        suggested_query = self.suggested_query

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query_id": query_id,
                "chunks": chunks,
                "stripped_query": stripped_query,
            }
        )
        if pipeline_logs is not UNSET:
            field_dict["pipeline_logs"] = pipeline_logs
        if suggested_query is not UNSET:
            field_dict["suggested_query"] = suggested_query

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_id = d.pop("query_id")

        chunks = []
        _chunks = d.pop("chunks")
        for chunks_item_data in _chunks:
            chunks_item = ChunkResult.from_dict(chunks_item_data)

            chunks.append(chunks_item)

        stripped_query = cast(List[str], d.pop("stripped_query"))

        pipeline_logs: Union[SearchResultPipelineLogs, Unset] = UNSET
        _pipeline_logs = d.pop("pipeline_logs", UNSET)
        if not isinstance(_pipeline_logs, Unset):
            pipeline_logs = SearchResultPipelineLogs.from_dict(_pipeline_logs)

        suggested_query = d.pop("suggested_query", UNSET)

        search_result_chunks = cls(
            query_id=query_id,
            chunks=chunks,
            stripped_query=stripped_query,
            pipeline_logs=pipeline_logs,
            suggested_query=suggested_query,
        )

        search_result_chunks.additional_properties = d
        return search_result_chunks

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
