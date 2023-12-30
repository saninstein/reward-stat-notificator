import time
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

from web3 import Web3, HTTPProvider, WebsocketProvider
from web3.contract.contract import ContractEvent
from web3.providers.auto import WS_SCHEMES, HTTP_SCHEMES
from web3.types import EventData

from app.utils import retry_call


def get_w3(uri: str) -> Web3:
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme in WS_SCHEMES:
        provider = WebsocketProvider(uri)
    elif parsed_uri.scheme in HTTP_SCHEMES:
        provider = HTTPProvider(uri)
    else:
        raise ValueError(f'Protocol "{parsed_uri.scheme}" is not supported.')

    return Web3(provider)


def get_events(
    contract_event: ContractEvent,
    from_block: int = 0,
    to_block: Optional[int] = None,
    request_limit: int = 10_000,
    argument_filters: Optional[Dict[str, Any]] = None,
    request_period: Optional[int] = None
) -> List[EventData]:
    """
    Returns events of type 'contract_event' from 'from_block' block number to
    'to_block' block number (both are inclusive), 'request_limit' is a count of observable
    blocks per one request.

    :param contract_event: event to fetch
    :param from_block: start block number
    :param to_block: end block number
    :param request_limit: logs per request
    :param request_period: time (in seconds) to wait between log fetch requests
    """
    if to_block is None:
        to_block = retry_call(lambda: contract_event.w3.eth.block_number)
    else:
        assert from_block <= to_block, f'Should be {from_block} <= {to_block}'

    events = []

    request_start = None
    while from_block <= to_block:
        if request_start and request_period:
            time_spent = time.time() - request_start
            if time_spent < request_period:
                time.sleep(request_period - time_spent)

        batch_to_block = min(from_block + request_limit - 1, to_block)
        # eth_getLogs (fromBlock and toBlock are inclusive)
        try:
            request_start = time.time()
            events.extend(
                retry_call(
                    lambda: contract_event.get_logs(
                        fromBlock=from_block, toBlock=batch_to_block, argument_filters=argument_filters
                    )
                )
            )
        except ValueError as e:
            message = get_web3_error_message(e)
            if message and message.startswith('exceed maximum block range:'):
                request_limit = int(message.replace('exceed maximum block range: ', ''))
                continue
            raise
        from_block = batch_to_block + 1
    return events


def get_web3_error_message(e: ValueError) -> Optional[str]:
    """
    Get error message from web3 call
    :param e: call exception
    :return: error message
    """
    arg = e.args[0]
    message = None
    if isinstance(arg, dict):
        if 'message' in arg:
            message = arg['message']
        elif 'error' in arg:
            message = arg['error']
    elif isinstance(arg, str):
        message = arg
    return message
