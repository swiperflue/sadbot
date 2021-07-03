"""Letsdo bot command"""

from typing import Optional, List

from sadbot.command_interface import CommandInterface, BOT_HANDLER_TYPE_MESSAGE
from sadbot.message import Message
from sadbot.bot_reply import BotAction, BOT_ACTION_TYPE_REPLY_TEXT


class LetsdoBotCommand(CommandInterface):
    """This is the letsdo bot command class"""

    @property
    def handler_type(self) -> str:
        """Returns the type of event handled by the command"""
        return BOT_HANDLER_TYPE_MESSAGE

    @property
    def command_regex(self) -> str:
        """Returns the regex for matching letsdo commands"""
        return r"((!|\.)([Ll][Ee][Tt][Ss][Dd][Oo]\s+\w+))"

    def get_reply(self, message: Optional[Message] = None) -> Optional[List[BotAction]]:
        """Returns letsdo"""
        this = message.text[8:]
        this = (
            f"let's do {this}! {this} {this} toe "
            f"{this} banana fanna foe f{this[1:]} "
            f"me my moe m{this[1:]}, {this}"
        )
        return [BotAction(BOT_ACTION_TYPE_REPLY_TEXT, reply_text=this)]
