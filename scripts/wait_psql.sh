#!/bin/sh

# Extrai host e porta do DATABASE_URL
DATABASE_URL=${DATABASE_URL:-""}
if [ -z "$DATABASE_URL" ]; then
    echo "DATABASE_URL não definida."
    exit 1
fi

# Extrai o host e a porta
POSTGRES_HOST=$(echo $DATABASE_URL | sed -E 's|.*://[^@]+@([^:/]+):([0-9]+).*|\1|')
POSTGRES_PORT=$(echo $DATABASE_URL | sed -E 's|.*://[^@]+@([^:/]+):([0-9]+).*|\2|')

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT)..."
    sleep 2
done

echo "Postgres Database Started Successfully ($POSTGRES_HOST $POSTGRES_PORT)"