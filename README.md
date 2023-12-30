## Example `.env`
```
LOGGING_LEVEL=DEBUG
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db

ETH_RPC=https://eth.llamarpc.com
CONTRACT_ADDRESS=0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0
INITIAL_BLOCK=18889166  # block to start synchronization from

TG_BOT_TOKEN=123
TG_CHANEL_ID=123

NOTIFY_INTERVAL_SECONDS=14400
```

## Start app
Fill the `.env` file

```shell
> docker-compose up -d
```

## Tests
```shell
> pip install -r requirements.txt
> ./run-tests.sh
```
