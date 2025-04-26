#!/bin/bash

# Wait for PostgreSQL (using pg_isready instead of nc)
while ! pg_isready -h postgres-master -p 5434 -U postgres -d banksystem -t 1; do
  echo "Waiting for PostgreSQL master..."
  sleep 2
done

# Apply migrations
python manage.py migrate

# Start the main command
exec "$@"