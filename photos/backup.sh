docker exec -t immich_postgres pg_dumpall --clean --if-exists --username=postgres |
  # gzip >"/mnt/backup/$(date +%F-%R)postgres.sql.gz"
  gzip >"$(date +%F-%R)postgres.sql.gz"
