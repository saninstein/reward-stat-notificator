
# Generated by CodiumAI


from app.notificator import get_notificator, ConsoleNotificator, TelegramNotificator


class TestGetNotificator:

    #  Returns a ConsoleNotificator instance when no token and channel are provided
    def test_no_token_and_channel(self):
        notificator = get_notificator()
        assert isinstance(notificator, ConsoleNotificator)

    #  Returns a TelegramNotificator instance when token and channel are provided
    def test_token_and_channel(self, mocker):
        mocker.patch('app.notificator.Bot')
        notificator = get_notificator(token="TOKEN", channel=12345)
        assert isinstance(notificator, TelegramNotificator)

    #  Returns a ConsoleNotificator instance when only token is provided
    def test_only_token(self):
        notificator = get_notificator(token="TOKEN")
        assert isinstance(notificator, ConsoleNotificator)

    #  Returns a ConsoleNotificator instance when only channel is provided
    def test_only_channel(self):
        notificator = get_notificator(channel=12345)
        assert isinstance(notificator, ConsoleNotificator)

    #  Returns a ConsoleNotificator instance when token is an empty string
    def test_empty_token(self):
        notificator = get_notificator(token="")
        assert isinstance(notificator, ConsoleNotificator)