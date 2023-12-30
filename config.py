import logging
import os

from eth_utils import to_checksum_address

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
logging.basicConfig(level=logging.getLevelNamesMapping()[LOGGING_LEVEL])

ETH_RPC = os.environ.get('ETH_RPC', 'https://eth.llamarpc.com')
CONTRACT_ADDRESS = to_checksum_address(os.environ.get('CONTRACT_ADDRESS', '0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0'))
INITIAL_BLOCK = int(os.environ.get('INITIAL_BLOCK', 18889166))

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'db')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'db_user')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
TG_CHANEL_ID = os.environ.get('TG_CHANEL_ID')

NOTIFY_INTERVAL_SECONDS = int(os.environ.get('NOTIFY_INTERVAL_SECONDS', 30))
