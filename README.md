# sadbot
A simple telegram bot.  
Which main feature is its sed command, the famous UNIX command.

## Dependencies
The bot has the following dependencies:
- `requests`
- `html2text`
- `pillow`

Which can be installed with:
```
pip3 install -r requirements.txt \
             -r dev-requirements.txt # Add this when developing the bot
```
The captcha command may depend on `fonts-freefont-ttf`, which can be installed
via:
```shell
sudo apt install fonts-freefont-ttf
```

## Installation
You have to place your bot token either in the environment variables or in the
config files, by manually editing them:
```
nano sadbot/config.py
nano Dockerfile # If you are using Docker/Podman
```
In the `sadbot/config.py` file you can also find the settings for configurable
bot commands (like `cringe`, `roulette` etc.)


## Usage
### Manual
Here's how you run the bot manually:  
```
nohup PYTHONPATH=. python3 -m sadbot & disown
```
### Systemd Service
Alternatively, you can create a new systemd service, which handles the bot
restart in a way more neat way, with these commands:
```shell
sed -i 's/userplaceholder/BOTUSER' sadbot.service
sed -i 's/pathplaceholder/BOTPATH' sadbot.service
sudo cp sadbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo service sadbot start
```
And to check the bot status you can simply type:
```shell
sudo service sadbot status
```
or, for reading the full log:
```shell
sudo journalctl -u sadbot.service
```
### Docker/Podman
If you like docker or podman, you can easily build the container using the
Dockerfile:
```shell
sudo docker build -m sadbot .
```
Then you can easily start the bot with:
```shell
sudo docker run -it sadbot
```

### NixOS
If you use NixOS you can easily build the project using the `default.nix` file:
```sh
nix-build
```
Then you can start the bot with:
```sh
./result/bin/sadbot
```
Don't forget to setup the token.


## Contributing
Pull requests are welcome.  
It's recommended to use `pylint`, `black` and `mypy` to check and review the
code before submitting it. You can set up all these three by enabling
`pre-commit`:
```shell
pre-commit install
```

### Writing a new bot command
If you want to add a new command you just have to write a new module file in the
commands directory.  
Here is a sample bot command, `sample_command.py`, it's code is pretty
self-explanatory:
```python3
"""Sample/uwuspeak bot command"""
# this import is required in every module:
from typing import Optional, List

# this imports is optional:
import re


# this imports is optional:
from sadbot.message_repository import MessageRepository

# you need to import the handler type, every command is tied to just one type
from sadbot.command_interface import CommandInterface, BOT_HANDLER_TYPE_MESSAGE
from sadbot.message import Message

# then you need to import the bot action type
from sadbot.bot_action import BotAction, BOT_ACTION_TYPE_REPLY_IMAGE


# the class name must be the pascal case of the module filename + "BotCommand"
class UwuBotCommand(CommandInterface):
    """This is the sample command bot command class"""

    # the constructor is NOT required. Anyway if the bot command need some
    # dependencies, they will be automatically injected through it
    def __init__(self, message_repository: MessageRepository):
        """Initializes the command class"""
        self.message_repository = message_repository

    @property
    def handler_type(self) -> int:
        """Here is the type of event handled by the command"""
        return BOT_HANDLER_TYPE_MESSAGE

    @property
    def command_regex(self) -> str:
        """Here is the regex that triggers this bot command"""
        regex = r"uwu(.*)?"
        return regex

    def get_reply(self, message: Optional[Message] = None) -> Optional[List[BotAction]]:
        """This function can return some bot actions/replies that will  be sent later"""
        # this is an example on how you can process the message that triggered
        # the command to get a custom reply
        # here we are  getting the last message sent in the chat with the support of
        # a very useful module of sadbot we're injecting into this class
        # we could also have injected the direct database connection and retrieved
        # the last message directly
        if message is None:
            return None
        previous_message = self.message_repository.get_previous_message(
            message, r"^(?!\s*$).+"
        )
        if previous_message is None:
            return None
        if previous_message.text is None:
            return None
        try:
            # uwu-mocking the message found
            reply_text = re.sub(r"(\w{3})", r"\1w", previous_message.text)
        except re.error:
            return None
        # here is how you open/set an image for the bot action
        with open("./sadbot/data/uwu.jpg", mode="rb") as reply_image_file:
            reply_image = reply_image_file.read()
        return [
            BotAction(
                BOT_ACTION_TYPE_REPLY_IMAGE,
                reply_image=reply_image,
                reply_text=reply_text,
            )
        ]
```

### Managers
Managers are used for handling sent messages/actions and to perform actions
at specific moments.
Managers are called indirectly by the commands, through the `BotAction`
attribute `reply_callback_manager_name`.
Additional info may be passed by the commands to the managers by through the
`BotAction` attribute `reply_callback_manager_info`
So when a manager triggered, it's `handle_callback` function will be called and
it will be given as parameters:
- the message that triggered the command
- the optional outgoing message/reply that triggered the manager
- the optional callback info

During the bot startup, every manager is initialized.
Managers may behave like containers for multiple sub-managers.

## Todo list
- [ ] Antiflood, samewords count and newlines count
- [ ] Outgoing messages queue
- [ ] Reminder tag/bookmark command
- [ ] VC Radio
- [ ] Group admin settings: enabled modules etc.
- [ ] Add new tables: for images, for edits and for usernames
- [X] Add media support for outgoing messages
- [X] Fix the roulette code
- [X] Seen command
- [X] User ratelimit
- [X] Group ratelimit
- [X] FBI watchlist
- [X] Captcha command
- [X] Translate command
- [X] Asynchronous processing <- HIGH PRIORITY | Multithreading
- [X] Welcome messages
- [X] Big chan url pictures
- [X] Beaver command
- [X] Stay cool on weed questions
- [X] Multiple messages per command (return a list)
- [X] Chat events handlers
- [X] Mute command
- [X] Ban command
- [X] Kick command
- [X] MyPy cleanup
- [X] Rewrite managers
- [X] BOT_ACTION_NONE
