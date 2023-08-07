from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractTopChunk")


@attr.s(auto_attribs=True)
class ExtractTopChunk:
    """ Top chunk schema to be returned from the API. """

    rank: int
    chunk_id: str
    page: int
    text: str
    distance: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rank = self.rank
        chunk_id = self.chunk_id
        page = self.page
        text = self.text
        distance = self.distance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rank": rank,
                "chunk_id": chunk_id,
                "page": page,
                "text": text,
            }
        )
        if distance is not UNSET:
            field_dict["distance"] = distance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rank = d.pop("rank")

        chunk_id = d.pop("chunk_id")

        page = d.pop("page")

        text = d.pop("text")

        distance = d.pop("distance", UNSET)

        extract_top_chunk = cls(
            rank=rank,
            chunk_id=chunk_id,
            page=page,
            text=text,
            distance=distance,
        )

        extract_top_chunk.additional_properties = d
        return extract_top_chunk

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
