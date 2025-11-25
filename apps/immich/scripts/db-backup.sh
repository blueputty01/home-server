# back up immich database
docker exec -t immich_postgres pg_dumpall --clean --if-exists --username=postgres |
  gzip >"/mnt/backup/immich/$(date +%F-%R)postgres.sql.gz"