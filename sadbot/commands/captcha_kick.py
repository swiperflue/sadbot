"""Captcha kick bot command"""

from typing import Optional, List
import random
import logging

from sadbot.command_interface import CommandInterface, BOT_HANDLER_TYPE_CALLBACK_QUERY
from sadbot.message import Message
from sadbot.bot_action import (
    BotAction,
    BOT_ACTION_TYPE_BAN_USER,
    BOT_ACTION_TYPE_UNBAN_USER,
    BOT_ACTION_TYPE_ANSWER_CALLBACK_QUERY,
    BOT_ACTION_TYPE_REPLY_TEXT,
    BOT_ACTION_TYPE_REPLY_IMAGE,
    BOT_ACTION_TYPE_DELETE_MESSAGE,
    BOT_ACTION_TYPE_RESTRICT_CHAT_MEMBER,
    BOT_ACTION_PRIORITY_HIGH,
)
from sadbot.app import App
from sadbot.classes.captcha import Captcha
from sadbot.classes.permissions import Permissions


class CaptchaKickBotCommand(CommandInterface):
    """This is the captcha bot command class"""

    def __init__(self, app: App, captcha: Captcha, permissions: Permissions):
        """Initializes the captcha command"""
        self.app = app
        self.captcha = captcha
        self.permissions = permissions

    @property
    def handler_type(self) -> int:
        return BOT_HANDLER_TYPE_CALLBACK_QUERY

    @property
    def command_regex(self) -> str:
        """Returns the regex for matching new users"""
        return r"captcha.*"

    @staticmethod
    def get_welcome_reply(new_user: str) -> str:
        """Returns a welcome reply"""
        welcome_replies = [
            f"Welcome {new_user}",
            f"!! Yooo welcome {new_user}",
            f"W-w-welcome {new_user} ~~",
        ]
        return random.choice(welcome_replies)

    @staticmethod
    def get_not_your_captcha_reply() -> str:
        """Returns a reply for a user solving someone else's captcha"""
        not_your_captcha_replies = [
            "That's not your captcha.",
            "Yoo tf you doing that ain't your business",
        ]
        return random.choice(not_your_captcha_replies)

    def get_reply(self, message: Optional[Message] = None) -> Optional[List[BotAction]]:
        """'Welcomes' a new user"""
        if message is None or message.text is None:
            return None
        callback_data = message.text.rsplit("-", 1)
        callback_data_split = callback_data[0].split("-", 1)
        captcha_id = callback_data_split[1]
        captcha_sender_id = captcha_id.split(".")[1]
        if captcha_sender_id != str(message.sender_id):
            not_yours = self.get_not_your_captcha_reply()
            return [
                BotAction(
                    BOT_ACTION_TYPE_ANSWER_CALLBACK_QUERY,
                    reply_callback_query_id=message.message_id,
                    reply_text=not_yours,
                    reply_priority=BOT_ACTION_PRIORITY_HIGH,
                )
            ]
        captcha_text = self.captcha.get_captcha_from_id(captcha_id)
        self.captcha.delete_captcha(captcha_id)
        if captcha_text is None:
            logging.warning("Error: captcha not found in the database.")
            return None
        if callback_data[1] == captcha_text:
            correct_captcha_replies = ["Correct.", "Yo! You got it right!", "uwu nice"]
            correct_captcha = random.choice(correct_captcha_replies)
            new_user = (
                message.sender_name
                if message.sender_username is None
                else f"@{message.sender_username}"
            )
            self.captcha.delete_captcha(captcha_id)
            welcome_reply = self.get_welcome_reply(new_user)
            permissions = self.permissions.get_user_permissions(
                message.sender_id, message.chat_id
            )
            if permissions is None:
                permissions = self.app.get_chat_permissions(message.chat_id)
            if message.chat_id == -1_001_127_994_403:
                with open("./sadbot/data/grules.jpg", mode="rb") as reply_image_file:
                    reply_image = reply_image_file.read()
                return [
                    BotAction(
                        BOT_ACTION_TYPE_ANSWER_CALLBACK_QUERY,
                        reply_callback_query_id=message.message_id,
                        reply_text=correct_captcha,
                        reply_priority=BOT_ACTION_PRIORITY_HIGH,
                    ),
                    BotAction(
                        BOT_ACTION_TYPE_REPLY_IMAGE,
                        reply_text=welcome_reply,
                        reply_image=reply_image,
                    ),
                    BotAction(
                        BOT_ACTION_TYPE_DELETE_MESSAGE,
                        reply_ban_user_id=message.sender_id,
                        reply_delete_message_id=message.reply_id,
                        reply_priority=BOT_ACTION_PRIORITY_HIGH,
                    ),
                    BotAction(
                        BOT_ACTION_TYPE_RESTRICT_CHAT_MEMBER,
                        reply_permissions=permissions,
                        reply_ban_user_id=message.sender_id,
                        reply_priority=BOT_ACTION_PRIORITY_HIGH,
                    ),
                ]
            return [
                BotAction(
                    BOT_ACTION_TYPE_ANSWER_CALLBACK_QUERY,
                    reply_callback_query_id=message.message_id,
                    reply_text=correct_captcha,
                    reply_priority=BOT_ACTION_PRIORITY_HIGH,
                ),
                BotAction(BOT_ACTION_TYPE_REPLY_TEXT, reply_text=welcome_reply),
                BotAction(
                    BOT_ACTION_TYPE_DELETE_MESSAGE,
                    reply_ban_user_id=message.sender_id,
                    reply_delete_message_id=message.reply_id,
                    reply_priority=BOT_ACTION_PRIORITY_HIGH,
                ),
                BotAction(
                    BOT_ACTION_TYPE_RESTRICT_CHAT_MEMBER,
                    reply_permissions=permissions,
                    reply_ban_user_id=message.sender_id,
                    reply_priority=BOT_ACTION_PRIORITY_HIGH,
                ),
            ]
        # return self.kick_user(message, captcha_id)
        return self.ask_user_to_join_again(message)

    @staticmethod
    def ask_user_to_join_again(message: Message) -> List[BotAction]:
        """Instead of kicking the user, this function asks to rejoin"""
        user = (
            message.sender_name
            if message.sender_username is None
            else f"@{message.sender_username}"
        )
        reply_text = (
            f"{user} if you want to talk here you have to rejoin the chat and get a new "
            f"captcha."
        )
        wrong_captcha = "Wrong captcha"
        return [
            BotAction(
                BOT_ACTION_TYPE_ANSWER_CALLBACK_QUERY,
                reply_callback_query_id=message.message_id,
                reply_text=wrong_captcha,
                reply_priority=BOT_ACTION_PRIORITY_HIGH,
            ),
            BotAction(
                BOT_ACTION_TYPE_REPLY_TEXT,
                reply_text=reply_text,
                reply_priority=BOT_ACTION_PRIORITY_HIGH,
            ),
            BotAction(
                BOT_ACTION_TYPE_DELETE_MESSAGE,
                reply_ban_user_id=message.sender_id,
                reply_delete_message_id=message.reply_id,
                reply_priority=BOT_ACTION_PRIORITY_HIGH,
            ),
        ]

    def kick_user(
        self,
        message: Message,
        captcha_id: str,
        answer_callback_query: Optional[bool] = True,
        sent_message_to_delete_id: Optional[int] = None,
    ) -> List[BotAction]:
        """Kicks a user from a chat"""
        new_user = (
            message.sender_name
            if message.sender_username is None
            else f"@{message.sender_username}"
        )
        kick_text_replies = [
            "Begone bot",
            "lol i knew it was a bot",
            "There's space for only one bot here, and that's me",
            "Wrong captcha",
            "Oopsie-whooppsie *blushes* owo s s s-owrry but the cawpthwa yowu enterwed was nwot "
            "corrwect ;-; *starts twerking*",
            "Get rekt",
        ]
        kick_text = random.choice(kick_text_replies)
        kick_text += f"\n(I kicked {new_user} (id {message.sender_id}))"
        self.captcha.delete_captcha(captcha_id)
        replies = []
        if answer_callback_query:
            replies.append(
                BotAction(
                    BOT_ACTION_TYPE_ANSWER_CALLBACK_QUERY,
                    reply_callback_query_id=message.message_id,
                    reply_text=kick_text,
                    reply_priority=BOT_ACTION_PRIORITY_HIGH,
                )
            )
        replies += [
            BotAction(
                BOT_ACTION_TYPE_BAN_USER,
                reply_ban_user_id=message.sender_id,
                reply_priority=BOT_ACTION_PRIORITY_HIGH,
            ),
            BotAction(
                BOT_ACTION_TYPE_REPLY_TEXT,
                reply_text=kick_text,
                reply_priority=BOT_ACTION_PRIORITY_HIGH,
            ),
            BotAction(
                BOT_ACTION_TYPE_UNBAN_USER,
                reply_ban_user_id=message.sender_id,
                reply_priority=BOT_ACTION_PRIORITY_HIGH,
            ),
        ]
        if sent_message_to_delete_id is not None:
            replies += [
                BotAction(
                    BOT_ACTION_TYPE_DELETE_MESSAGE,
                    reply_delete_message_id=sent_message_to_delete_id,
                    reply_priority=BOT_ACTION_PRIORITY_HIGH,
                )
            ]
        return replies
