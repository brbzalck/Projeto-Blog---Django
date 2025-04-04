# O commands.sh garante que o banco esteja pronto, 
# aplica as configurações do Django e roda o servidor.

#!/bin/sh

# define que é um script shell, e se der problema deve parar
set -e

# shell script que espera o postgres ficar diponível antes do continuar, para não dar erros
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT)..."
    sleep 0.1
done

echo "Postgres Database Started Successfully ($POSTGRES_HOST $POSTGRES_PORT)"

# coleta os arquivos estaticos
python manage.py collectstatic
# Aplica as migrações no banco de dados
python manage.py migrate
# roda o server
python manage.py runserver