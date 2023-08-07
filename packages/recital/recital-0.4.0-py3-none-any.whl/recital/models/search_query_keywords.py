from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.search_query_keywords_filters import SearchQueryKeywordsFilters
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchQueryKeywords")


@attr.s(auto_attribs=True)
class SearchQueryKeywords:
    """ Schema for keyword search queries. """

    folder_ids: Union[Unset, List[int]] = UNSET
    filters: Union[SearchQueryKeywordsFilters, Unset] = UNSET
    keywords: Union[Unset, List[str]] = UNSET
    keyword_op: Union[Unset, None] = UNSET
    file_ids: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folder_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.folder_ids, Unset):
            folder_ids = self.folder_ids

        filters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        keywords: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = self.keywords

        keyword_op: Union[Unset, str] = UNSET
        if not isinstance(self.keyword_op, Unset):
            keyword_op = self.keyword_op

        file_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.file_ids, Unset):
            file_ids = self.file_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if folder_ids is not UNSET:
            field_dict["folder_ids"] = folder_ids
        if filters is not UNSET:
            field_dict["filters"] = filters
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if keyword_op is not UNSET:
            field_dict["keyword_op"] = keyword_op
        if file_ids is not UNSET:
            field_dict["file_ids"] = file_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_ids = cast(List[int], d.pop("folder_ids", UNSET))

        filters: Union[SearchQueryKeywordsFilters, Unset] = UNSET
        _filters = d.pop("filters", UNSET)
        if not isinstance(_filters, Unset):
            filters = SearchQueryKeywordsFilters.from_dict(_filters)

        keywords = cast(List[str], d.pop("keywords", UNSET))

        keyword_op = d.pop("keyword_op", UNSET)

        file_ids = cast(List[int], d.pop("file_ids", UNSET))

        search_query_keywords = cls(
            folder_ids=folder_ids,
            filters=filters,
            keywords=keywords,
            keyword_op=keyword_op,
            file_ids=file_ids,
        )

        search_query_keywords.additional_properties = d
        return search_query_keywords

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
