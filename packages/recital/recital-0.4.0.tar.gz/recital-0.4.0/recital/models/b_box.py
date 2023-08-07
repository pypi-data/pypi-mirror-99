from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BBox")


@attr.s(auto_attribs=True)
class BBox:
    """  """

    x_min: float
    y_min: float
    x_max: float
    y_max: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        x_min = self.x_min
        y_min = self.y_min
        x_max = self.x_max
        y_max = self.y_max

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        x_min = d.pop("x_min")

        y_min = d.pop("y_min")

        x_max = d.pop("x_max")

        y_max = d.pop("y_max")

        b_box = cls(
            x_min=x_min,
            y_min=y_min,
            x_max=x_max,
            y_max=y_max,
        )

        b_box.additional_properties = d
        return b_box

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
