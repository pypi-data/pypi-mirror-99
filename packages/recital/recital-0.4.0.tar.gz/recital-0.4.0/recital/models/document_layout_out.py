from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.document_layout_item import DocumentLayoutItem

T = TypeVar("T", bound="DocumentLayoutOut")


@attr.s(auto_attribs=True)
class DocumentLayoutOut:
    """ "Document Layout schema for the GET route """

    layout: List[DocumentLayoutItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        layout = []
        for layout_item_data in self.layout:
            layout_item = layout_item_data.to_dict()

            layout.append(layout_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "layout": layout,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        layout = []
        _layout = d.pop("layout")
        for layout_item_data in _layout:
            layout_item = DocumentLayoutItem.from_dict(layout_item_data)

            layout.append(layout_item)

        document_layout_out = cls(
            layout=layout,
        )

        document_layout_out.additional_properties = d
        return document_layout_out

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
