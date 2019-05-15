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
    # DB Type: dw
    # Total Memory (RAM): 64 GB
    # CPUs num: 4
    # Data Storage: ssd

    ALTER SYSTEM SET max_connections = '20';
    ALTER SYSTEM SET shared_buffers = '16GB';
    ALTER SYSTEM SET effective_cache_size = '48GB';
    ALTER SYSTEM SET maintenance_work_mem = '2GB';
    ALTER SYSTEM SET checkpoint_completion_target = '0.9';
    ALTER SYSTEM SET wal_buffers = '16MB';
    ALTER SYSTEM SET default_statistics_target = '500';
    ALTER SYSTEM SET random_page_cost = '1.1';
    ALTER SYSTEM SET effective_io_concurrency = '200';
    ALTER SYSTEM SET work_mem = '209715kB';
    ALTER SYSTEM SET min_wal_size = '4GB';
    ALTER SYSTEM SET max_wal_size = '8GB';
    ALTER SYSTEM SET max_worker_processes = '4';
    ALTER SYSTEM SET max_parallel_workers_per_gather = '2';
    ALTER SYSTEM SET max_parallel_workers = '4';
EOSQL
}

alter_system
