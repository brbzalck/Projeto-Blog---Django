#!/bin/sh

# Extrai host e porta da DATABASE_URL (formato padrão do Render)
export POSTGRES_HOST=$(echo $DATABASE_URL | sed -E 's|postgres://[^@]+@([^:/]+):[0-9]+/.*|\1|')
export POSTGRES_PORT=$(echo $DATABASE_URL | sed -E 's|postgres://[^@]+@[^:/]+:([0-9]+)/.*|\1|')

# Espera o banco de dados iniciar
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "⏳ Aguardando o banco de dados ($POSTGRES_HOST:$POSTGRES_PORT)..."
    sleep 2
done

echo "✅ Banco de dados iniciado com sucesso ($POSTGRES_HOST:$POSTGRES_PORT)"
