from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extract_paragraph_config import ExtractParagraphConfig
from ..models.extract_question_config import ExtractQuestionConfig
from ..models.extract_type import ExtractType
from ..models.extract_value_config import ExtractValueConfig
from ..types import Unset

T = TypeVar("T", bound="DeprecatedExtractModelCreate")


@attr.s(auto_attribs=True)
class DeprecatedExtractModelCreate:
    """ Deprecated. """

    config: Union[ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]
    name: str
    type: ExtractType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self.config, ExtractValueConfig):
            config = self.config.to_dict()

        elif isinstance(self.config, ExtractParagraphConfig):
            config = self.config.to_dict()

        else:
            config = self.config.to_dict()

        name = self.name
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
                "name": name,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_config(data: Any) -> Union[ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]:
            data = None if isinstance(data, Unset) else data
            config: Union[ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]
            try:
                config = ExtractValueConfig.from_dict(data)

                return config
            except:  # noqa: E722
                pass
            try:
                config = ExtractParagraphConfig.from_dict(data)

                return config
            except:  # noqa: E722
                pass
            config = ExtractQuestionConfig.from_dict(data)

            return config

        config = _parse_config(d.pop("config"))

        name = d.pop("name")

        type = ExtractType(d.pop("type"))

        deprecated_extract_model_create = cls(
            config=config,
            name=name,
            type=type,
        )

        deprecated_extract_model_create.additional_properties = d
        return deprecated_extract_model_create

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
