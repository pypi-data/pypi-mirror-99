import datetime
from typing import Any, ClassVar, Dict, List, Type, TypeVar, Union, type_check_only
from typing_extensions import Final, Protocol

from .colour import Colour
from .http import _EmbedDict

class _EmptyEmbed:
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...

EmptyEmbed: Final[_EmptyEmbed]

class EmbedProxy:
    def __init__(self, layer: Dict[str, Any]) -> None: ...
    def __len__(self) -> int: ...
    def __getattr__(self, attr: str) -> _EmptyEmbed: ...

_E = TypeVar('_E', bound=Embed)

# TODO: remove this comment when a new version of black comes out
@type_check_only
class _EmbedFooterData(Protocol):
    text: Union[str, _EmptyEmbed]
    icon_url: Union[str, _EmptyEmbed]

@type_check_only
class _EmbedImageData(Protocol):
    url: Union[str, _EmptyEmbed]
    proxy_url: Union[str, _EmptyEmbed]
    height: Union[int, _EmptyEmbed]
    width: Union[int, _EmptyEmbed]

@type_check_only
class _EmbedVideoData(Protocol):
    url: Union[str, _EmptyEmbed]
    height: Union[int, _EmptyEmbed]
    width: Union[int, _EmptyEmbed]

@type_check_only
class _EmbedProviderData(Protocol):
    name: Union[str, _EmptyEmbed]
    url: Union[str, _EmptyEmbed]

@type_check_only
class _EmbedAuthorData(Protocol):
    name: Union[str, _EmptyEmbed]
    url: Union[str, _EmptyEmbed]
    icon_url: Union[str, _EmptyEmbed]
    proxy_icon_url: Union[str, _EmptyEmbed]

@type_check_only
class _EmbedFieldData(Protocol):
    name: Union[str, _EmptyEmbed]
    value: Union[str, _EmptyEmbed]
    inline: Union[bool, _EmptyEmbed]

class Embed:
    title: Union[str, _EmptyEmbed]
    type: str
    description: Union[str, _EmptyEmbed]
    url: Union[str, _EmptyEmbed]
    colour: Union[int, Colour, _EmptyEmbed]
    color: Union[int, Colour, _EmptyEmbed]
    timestamp: Union[datetime.datetime, _EmptyEmbed]

    Empty: ClassVar[_EmptyEmbed] = ...
    def __init__(
        self,
        *,
        color: Union[int, Colour, _EmptyEmbed] = ...,
        colour: Union[int, Colour, _EmptyEmbed] = ...,
        title: Union[str, _EmptyEmbed] = ...,
        type: str = ...,
        url: Union[str, _EmptyEmbed] = ...,
        description: Union[str, _EmptyEmbed] = ...,
        timestamp: Union[datetime.datetime, _EmptyEmbed] = ...,
    ) -> None: ...
    @classmethod
    def from_dict(cls: Type[_E], data: _EmbedDict) -> _E: ...
    def copy(self) -> Embed: ...
    def __len__(self) -> int: ...
    @property
    def footer(self) -> _EmbedFooterData: ...
    def set_footer(
        self: _E,
        *,
        text: Union[str, _EmptyEmbed] = ...,
        icon_url: Union[str, _EmptyEmbed] = ...,
    ) -> _E: ...
    @property
    def image(self) -> _EmbedImageData: ...
    def set_image(self: _E, *, url: Union[str, _EmptyEmbed]) -> _E: ...
    @property
    def thumbnail(self) -> _EmbedImageData: ...
    def set_thumbnail(self: _E, *, url: Union[str, _EmptyEmbed]) -> _E: ...
    @property
    def video(self) -> _EmbedVideoData: ...
    @property
    def provider(self) -> _EmbedProviderData: ...
    @property
    def author(self) -> _EmbedAuthorData: ...
    def set_author(
        self: _E,
        *,
        name: str,
        url: Union[str, _EmptyEmbed] = ...,
        icon_url: Union[str, _EmptyEmbed] = ...,
    ) -> _E: ...
    def remove_author(self: _E) -> _E: ...
    @property
    def fields(self) -> List[_EmbedFieldData]: ...
    def add_field(self: _E, *, name: str, value: str, inline: bool = ...) -> _E: ...
    def insert_field_at(
        self: _E, index: int, *, name: str, value: str, inline: bool = ...
    ) -> _E: ...
    def clear_fields(self) -> None: ...
    def remove_field(self, index: int) -> None: ...
    def set_field_at(
        self: _E, index: int, *, name: str, value: str, inline: bool = ...
    ) -> _E: ...
    def to_dict(self) -> _EmbedDict: ...
