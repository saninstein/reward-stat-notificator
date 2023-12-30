from datetime import datetime
from logging import Logger
from typing import List, Optional

from eth_typing import Address
from eth_utils import to_checksum_address
from sqlalchemy import func
from web3 import Web3
from web3.contract import Contract
from web3.types import EventData

from app.abi import ABI
from app.eth import get_w3, get_events
from app.models import Distribution
from app.utils import get_class_logger, retry_call
from config import INITIAL_BLOCK
from db.sessions import db_session


class DistributionEventsSynchronizer:
    logger: Logger
    _contract: Contract
    _w3: Web3
    __latest_processed_block: Optional[int] = None

    def __init__(self, rpc_uri: str, address: Address):
        self._w3 = get_w3(rpc_uri)
        self._contract = self._w3.eth.contract(address=address, abi=ABI)
        self.logger = get_class_logger(self)

    @property
    def _latest_processed_block(self) -> int:
        """
        Returns tuple of checkpoints: latest processed block and transactions set
        """
        if self.__latest_processed_block is None:
            with db_session() as session:
                block_number = session.query(func.max(Distribution.block)).scalar()

            self._latest_processed_block = block_number or INITIAL_BLOCK

        return self.__latest_processed_block

    @_latest_processed_block.setter
    def _latest_processed_block(self, block_number: int):
        self.logger.debug(f'Set _latest_processed_block to: {block_number}')
        self.__latest_processed_block = block_number

    def _save_events(self, events: List[EventData]):
        events_instances = []
        e: EventData
        for e in events:
            event_instance = Distribution()
            event_instance.block = e['blockNumber']
            event_instance.transaction = e['transactionHash'].hex()
            event_instance.sender = to_checksum_address(
                retry_call(
                    lambda: self._w3.eth.get_transaction(e['transactionHash'])['from']
                )
            )
            event_instance.timestamp = datetime.utcfromtimestamp(
                retry_call(
                    lambda: self._w3.eth.get_block(e['blockNumber'])['timestamp']
                )
            )
            event_instance.input_aix = e['args']['inputAixAmount']
            event_instance.distributed_aix = e['args']['distributedAixAmount']
            event_instance.swapped_eth = e['args']['swappedEthAmount']
            event_instance.distributed_eth = e['args']['distributedEthAmount']

            events_instances.append(event_instance)

        with db_session() as session:
            session.add_all(events_instances)
            session.commit()

        if events:
            self._latest_processed_block = events[-1]['blockNumber']

        self.logger.debug(f'Latest event {events[-1:]}')
        self.logger.info(f'Added {len(events_instances)} events')

    def sync(self, up_to_block: Optional[int] = None):
        self.logger.debug(f'Start sync from: {self._latest_processed_block} to: {up_to_block}')

        events = get_events(
            self._contract.events.TotalDistribution,
            from_block=self._latest_processed_block + 1,
            to_block=up_to_block,
            request_period=1
        )

        self._save_events(events)
