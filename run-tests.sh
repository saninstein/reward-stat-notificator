#!/usr/bin/env bash

set -a
cat > .env.test << EOT
POSTGRES_HOST=0.0.0.0
POSTGRES_PORT=5433
POSTGRES_DB=test
POSTGRES_USER=user
POSTGRES_PASSWORD=password
ETH_RPC=https://eth.llamarpc.com
CONTRACT_ADDRESS=0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0
EOT
docker run -d --rm --name test-db -p 5433:5432 --env-file .env.test postgres:12-alpine
docker exec test-db bash -c 'until pg_isready; do sleep 1; done'
sleep 1
source .env.test
alembic upgrade heads
sleep 1
python -m pytest
status=$?
docker stop test-db
set +a
[ $status -eq 0 ] || exit 1
