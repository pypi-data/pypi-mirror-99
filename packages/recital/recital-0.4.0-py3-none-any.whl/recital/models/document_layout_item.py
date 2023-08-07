from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.document_layout_item_coordinates import DocumentLayoutItemCoordinates
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentLayoutItem")


@attr.s(auto_attribs=True)
class DocumentLayoutItem:
    """ "Document Layout Item schema for the GET route """

    id: int
    elastic_id: str
    type: List[str]
    coordinates: DocumentLayoutItemCoordinates
    page: List[int]
    content: str
    related: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        elastic_id = self.elastic_id
        type = self.type

        coordinates = self.coordinates.to_dict()

        page = self.page

        content = self.content
        related = self.related

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "elastic_id": elastic_id,
                "type": type,
                "coordinates": coordinates,
                "page": page,
                "content": content,
            }
        )
        if related is not UNSET:
            field_dict["related"] = related

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        elastic_id = d.pop("elastic_id")

        type = cast(List[str], d.pop("type"))

        coordinates = DocumentLayoutItemCoordinates.from_dict(d.pop("coordinates"))

        page = cast(List[int], d.pop("page"))

        content = d.pop("content")

        related = d.pop("related", UNSET)

        document_layout_item = cls(
            id=id,
            elastic_id=elastic_id,
            type=type,
            coordinates=coordinates,
            page=page,
            content=content,
            related=related,
        )

        document_layout_item.additional_properties = d
        return document_layout_item

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
