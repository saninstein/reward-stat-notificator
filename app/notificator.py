from logging import Logger
from abc import ABCMeta, abstractmethod
from typing import Optional

from telegram import Bot

from app.utils import get_class_logger


class Notificator(metaclass=ABCMeta):
    """
    Abstract base class for sending notifications.
    """
    logger: Logger

    def __init__(self):
        self.logger = get_class_logger(self)

    @abstractmethod
    def send_message(self, message: str):
        """
        Sends text message to the channel.
        """
        raise NotImplementedError()


class ConsoleNotificator(Notificator):
    """
    Sends messages to std out. For the development purposes
    """
    def send_message(self, message: str):
        self.logger.info(f'Message: {message}')


class TelegramNotificator(Notificator):
    """
    Sends messages to telegram channel via BotApi
    """
    _bot: Bot
    _channel: int

    def __init__(self, token: str, channel: int):
        super().__init__()
        self._channel = channel
        self._bot = Bot(token)

    def send_message(self, message: str):
        self._bot.send_message(
            self._channel,
            message
        )


def get_notificator(token: Optional[str] = None, channel: Optional[int] = None) -> Notificator:
    if token and channel:
        return TelegramNotificator(token, channel)
    else:
        return ConsoleNotificator()
