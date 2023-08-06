from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.metadata_import_json_data import MetadataImportJSONData

T = TypeVar("T", bound="MetadataImportJSON")


@attr.s(auto_attribs=True)
class MetadataImportJSON:
    """ Schema representing metadata import expected in POST method. """

    data: MetadataImportJSONData
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = MetadataImportJSONData.from_dict(d.pop("data"))

        metadata_import_json = cls(
            data=data,
        )

        metadata_import_json.additional_properties = d
        return metadata_import_json

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
