from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.entity_in_db import EntityInDB

T = TypeVar("T", bound="ChunkEntities")


@attr.s(auto_attribs=True)
class ChunkEntities:
    """ Model for GET /chunk_entities endpoint. """

    id: str
    text: str
    entities: List[EntityInDB]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        text = self.text
        entities = []
        for entities_item_data in self.entities:
            entities_item = entities_item_data.to_dict()

            entities.append(entities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "text": text,
                "entities": entities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        text = d.pop("text")

        entities = []
        _entities = d.pop("entities")
        for entities_item_data in _entities:
            entities_item = EntityInDB.from_dict(entities_item_data)

            entities.append(entities_item)

        chunk_entities = cls(
            id=id,
            text=text,
            entities=entities,
        )

        chunk_entities.additional_properties = d
        return chunk_entities

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
