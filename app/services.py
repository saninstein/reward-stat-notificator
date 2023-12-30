import time
from abc import ABC, abstractmethod
from datetime import datetime
from logging import Logger
from threading import Thread

from web3 import Web3

from app.eth import get_w3
from app.events_syncronizer import DistributionEventsSynchronizer
from app.models import Distribution
from app.notificator import Notificator, get_notificator
from app.utils import get_class_logger, retry_call, readable_timedelta
from config import ETH_RPC, CONTRACT_ADDRESS, TG_BOT_TOKEN, TG_CHANEL_ID, NOTIFY_INTERVAL_SECONDS


class Service(Thread, ABC):
    """
    Base class for services.
    """
    logger: Logger
    sleep_between_ticks: int = 30

    def _init(self):
        """
        Service initializer
        """
        self.logger = get_class_logger(self)

    @abstractmethod
    def _tick(self):
        """
        Method calls every `sleep_between_ticks` seconds
        """
        raise NotImplementedError()

    def run(self):
        self._init()
        self.logger.info(f'Start service sleep_between_ticks: {self.sleep_between_ticks}')

        while True:
            try:
                self.logger.info('Start service tick')
                self._tick()
                self.logger.info('End service tick')
            except Exception as e:
                self.logger.exception(f'Unexpected error: {e}')
            time.sleep(self.sleep_between_ticks)


class SynchronizerService(Service):
    """
    Runs the DistributionEventsSynchronizer
    """
    _synchronizer: DistributionEventsSynchronizer

    def _init(self):
        super()._init()
        self._synchronizer = DistributionEventsSynchronizer(ETH_RPC, CONTRACT_ADDRESS)

    def _tick(self):
        self._synchronizer.sync()


class NotificatorService(Service):
    """
    Sends the daily statistics through Notificator
    """

    _notificator: Notificator
    _w3: Web3
    sleep_between_ticks = NOTIFY_INTERVAL_SECONDS

    def _init(self):
        super()._init()
        self._w3 = get_w3(ETH_RPC)
        self._notificator = get_notificator(TG_BOT_TOKEN, TG_CHANEL_ID)

    @staticmethod
    def _format_message(stat: dict) -> str:
        """
        Fills the message template
        :param stat: dict with the daily statistics
        :return: message string
        """
        now = datetime.utcnow()
        first_ts_pass = now - stat['first_ts']
        last_ts_pass = now - stat['last_ts']
        distributors = ' '.join(
            f'{address} ({balance:.2f} ETH)'
            for address, balance in zip(stat['distributors'], stat['balances'])
        )

        return f"""
        Daily $AIX Stats:
        - First TX: {readable_timedelta(first_ts_pass)} ago
        - Last TX: {readable_timedelta(last_ts_pass)} ago
        - AIX processed: {stat['total_input_aix']:,.2f}
        - AIX distributed: {stat['total_distributed_aix']:,.2f}
        - ETH bought: {stat['total_swapped_eth']:,.2f}
        - ETH distributed: {stat['total_distributed_eth']:,.2f}
        Distributors: {distributors}
        """

    def _tick(self):
        stat = Distribution.get_day_statistic(datetime.utcnow().date())
        if not stat['first_ts']:
            self.logger.info('No statistics')
            return

        stat['balances'] = [
            retry_call(lambda: self._w3.eth.get_balance(d) / 1e18)
            for d in stat['distributors']
        ]
        self._notificator.send_message(self._format_message(stat))
