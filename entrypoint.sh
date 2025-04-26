#!/bin/bash

# Wait for PostgreSQL master to be ready
while ! nc -z postgres-master 5434; do
  echo "Waiting for PostgreSQL master..."
  sleep 2
done

# Apply database migrations
python manage.py migrate

# Start server (or whatever command was passed)
exec "$@"