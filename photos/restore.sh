#!/bin/bash

read -p "Are you sure you want to restore from backup?" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
  docker compose down -v  # CAUTION! Deletes all Immich data to start from scratch
  ## Uncomment the next line and replace DB_DATA_LOCATION with your Postgres path to permanently reset the Postgres database
  # rm -rf DB_DATA_LOCATION # CAUTION! Deletes all Immich data to start from scratch
  docker compose pull             # Update to latest version of Immich (if desired)
  docker compose create           # Create Docker containers for Immich apps without running them
  docker start immich_postgres    # Start Postgres server
  sleep 10                        # Wait for Postgres server to start up
  # Check the database user if you deviated from the default
  gunzip --stdout "/path/to/backup/dump.sql.gz" \
  | sed "s/SELECT pg_catalog.set_config('search_path', '', false);/SELECT pg_catalog.set_config('search_path', 'public, pg_catalog', true);/g" \
  | docker exec -i immich_postgres psql --dbname=postgres --username=<DB_USERNAME>  # Restore Backup
  docker compose up -d            # Start remainder of Immich apps
fi

