"""This module contains the BotAction class"""

from typing import Optional, List, Dict
from dataclasses import dataclass

from sadbot.chat_permissions import ChatPermissions

BOT_ACTION_TYPE_REPLY_TEXT = 0
BOT_ACTION_TYPE_REPLY_IMAGE = 1
BOT_ACTION_TYPE_REPLY_AUDIO = 2
BOT_ACTION_TYPE_REPLY_VIDEO = 3
BOT_ACTION_TYPE_REPLY_FILE = 4
BOT_ACTION_TYPE_REPLY_VOICE = 5
BOT_ACTION_TYPE_BAN_USER = 6
BOT_ACTION_TYPE_INLINE_KEYBOARD = 7
BOT_ACTION_TYPE_ANSWER_CALLBACK_QUERY = 8
BOT_ACTION_TYPE_DELETE_MESSAGE = 9
BOT_ACTION_TYPE_RESTRICT_CHAT_MEMBER = 10
BOT_ACTION_TYPE_UNBAN_USER = 11
BOT_ACTION_TYPE_PROMOTE_CHAT_MEMBER = 12
BOT_ACTION_TYPE_NONE = 13
BOT_ACTION_PRIORITY_LOW = 0
BOT_ACTION_PRIORITY_MEDIUM = 1
BOT_ACTION_PRIORITY_HIGH = 2


@dataclass
class BotAction:  # pylint: disable=too-many-instance-attributes
    """BotAction class"""

    reply_type: int = BOT_ACTION_TYPE_REPLY_TEXT
    reply_text: Optional[str] = None
    reply_text_parsemode: Optional[str] = None
    reply_image: Optional[bytes] = None
    reply_video: Optional[bytes] = None
    reply_audio: Optional[bytes] = None
    reply_file: Optional[bytes] = None
    reply_voice: Optional[bytes] = None
    reply_ban_user_id: Optional[int] = None
    reply_inline_keyboard: Optional[List] = None
    reply_callback_query_id: Optional[int] = None
    reply_delete_message_id: Optional[int] = None
    reply_permissions: Optional[ChatPermissions] = None
    reply_restrict_until_date: int = 0
    reply_priority: int = BOT_ACTION_PRIORITY_LOW
    reply_callback_manager_name: Optional[str] = None
    reply_callback_manager_info: Optional[Dict] = None
    reply_chat_id: Optional[int] = None
    reply_to_message_id: Optional[int] = None
