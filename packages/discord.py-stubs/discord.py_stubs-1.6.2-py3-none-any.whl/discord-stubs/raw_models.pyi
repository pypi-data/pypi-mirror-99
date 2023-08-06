from typing import List, Optional, Set, type_check_only
from typing_extensions import Literal, TypedDict

from .http import _MessageDict, _PartialEmojiDict
from .member import Member
from .message import Message
from .partial_emoji import PartialEmoji

# TODO: remove this comment when a new version of black comes out
@type_check_only
class _BaseBulkMessageDeleteDict(TypedDict, total=False):
    guild_id: str

@type_check_only
class _BulkMessageDeleteDict(_BaseBulkMessageDeleteDict):
    ids: List[str]
    channel_id: str

@type_check_only
class _BaseReactionActionDict(TypedDict):
    message_id: str
    channel_id: str
    user_id: str
    emoji: _PartialEmojiDict

@type_check_only
class _ReactionActionDict(_BaseReactionActionDict, total=False):
    guild_id: str

@type_check_only
class _BaseReactionClearDict(TypedDict):
    channel_id: int
    message_id: int

@type_check_only
class _ReactionClearDict(_BaseReactionClearDict, total=False):
    guild_id: int

class _RawReprMixin: ...

class RawMessageDeleteEvent(_RawReprMixin):
    message_id: int
    channel_id: int
    guild_id: Optional[int]
    cached_message: Optional[Message]
    def __init__(self, data: _MessageDict) -> None: ...

class RawBulkMessageDeleteEvent(_RawReprMixin):
    message_ids: Set[int]
    channel_id: int
    guild_id: Optional[int]
    cached_messages: List[Message]
    def __init__(self, data: _BulkMessageDeleteDict) -> None: ...

class RawMessageUpdateEvent(_RawReprMixin):
    message_id: int
    channel_id: int
    data: _MessageDict
    cached_message: Optional[Message]
    def __init__(self, data: _MessageDict) -> None: ...

class RawReactionActionEvent(_RawReprMixin):
    message_id: int
    channel_id: int
    user_id: int
    emoji: PartialEmoji
    member: Optional[Member]
    event_type: Literal['REACTION_ADD', 'REACTION_REMOVE']
    guild_id: Optional[int]
    def __init__(
        self,
        data: _ReactionActionDict,
        emoji: PartialEmoji,
        event_type: Literal['REACTION_ADD', 'REACTION_REMOVE'],
    ) -> None: ...

class RawReactionClearEvent(_RawReprMixin):
    message_id: int
    channel_id: int
    guild_id: Optional[int]
    def __init__(self, data: _ReactionClearDict) -> None: ...

class RawReactionClearEmojiEvent(_RawReprMixin):
    message_id: int
    channel_id: int
    guild_id: Optional[int]
    emoji: PartialEmoji
    def __init__(self, data: _ReactionClearDict, emoji: PartialEmoji) -> None: ...
