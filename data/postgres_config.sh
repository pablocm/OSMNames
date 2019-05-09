#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

function alter_system() {
    echo "Altering System parameters"
    PGUSER="$POSTGRES_USER" psql --dbname="$POSTGRES_DB" <<-EOSQL

    -- add your postgres configuration here
    -- recommended: https://pgtune.leopard.in.ua/
    -- with alter system option

    # DB Version: 11
    # OS Type: linux
    # DB Type: mixed
    # Total Memory (RAM): 12 GB
    # CPUs num: 2
    # Data Storage: hdd

    ALTER SYSTEM SET max_connections = '100';
    ALTER SYSTEM SET shared_buffers = '3GB';
    ALTER SYSTEM SET effective_cache_size = '9GB';
    ALTER SYSTEM SET maintenance_work_mem = '768MB';
    ALTER SYSTEM SET checkpoint_completion_target = '0.9';
    ALTER SYSTEM SET wal_buffers = '16MB';
    ALTER SYSTEM SET default_statistics_target = '100';
    ALTER SYSTEM SET random_page_cost = '4';
    ALTER SYSTEM SET effective_io_concurrency = '2';
    ALTER SYSTEM SET work_mem = '15728kB';
    ALTER SYSTEM SET min_wal_size = '1GB';
    ALTER SYSTEM SET max_wal_size = '2GB';
    ALTER SYSTEM SET max_worker_processes = '2';
    ALTER SYSTEM SET max_parallel_workers_per_gather = '1';
    ALTER SYSTEM SET max_parallel_workers = '2';
EOSQL
}

alter_system
