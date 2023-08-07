from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extract_paragraph_config import ExtractParagraphConfig
from ..models.extract_question_config import ExtractQuestionConfig
from ..models.extract_value_config import ExtractValueConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="SynchronousExtractCreate")


@attr.s(auto_attribs=True)
class SynchronousExtractCreate:
    """ Schema for simple extract task generation """

    file_id: int
    config: Union[Unset, ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig] = UNSET
    model_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id
        config: Union[Unset, ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]
        if isinstance(self.config, Unset):
            config = UNSET
        elif isinstance(self.config, ExtractValueConfig):
            config = UNSET
            if not isinstance(self.config, Unset):
                config = self.config.to_dict()

        elif isinstance(self.config, ExtractParagraphConfig):
            config = UNSET
            if not isinstance(self.config, Unset):
                config = self.config.to_dict()

        else:
            config = UNSET
            if not isinstance(self.config, Unset):
                config = self.config.to_dict()

        model_id = self.model_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_id": file_id,
            }
        )
        if config is not UNSET:
            field_dict["config"] = config
        if model_id is not UNSET:
            field_dict["model_id"] = model_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_id = d.pop("file_id")

        def _parse_config(data: Any) -> Union[Unset, ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]:
            data = None if isinstance(data, Unset) else data
            config: Union[Unset, ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]
            try:
                config = UNSET
                _config = data
                if not isinstance(_config, Unset):
                    config = ExtractValueConfig.from_dict(_config)

                return config
            except:  # noqa: E722
                pass
            try:
                config = UNSET
                _config = data
                if not isinstance(_config, Unset):
                    config = ExtractParagraphConfig.from_dict(_config)

                return config
            except:  # noqa: E722
                pass
            config = UNSET
            _config = data
            if not isinstance(_config, Unset):
                config = ExtractQuestionConfig.from_dict(_config)

            return config

        config = _parse_config(d.pop("config", UNSET))

        model_id = d.pop("model_id", UNSET)

        synchronous_extract_create = cls(
            file_id=file_id,
            config=config,
            model_id=model_id,
        )

        synchronous_extract_create.additional_properties = d
        return synchronous_extract_create

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
