#!/bin/bash
set -e

# List of databases to create from the POSTGRES_ADDITIONAL_DB_NAMES environment variable
IFS=',' read -r -a DBS <<< "$POSTGRES_ADDITIONAL_DB_NAMES"

for db in "${DBS[@]}"; do
    echo "Creating database: $db"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $db;
EOSQL
done