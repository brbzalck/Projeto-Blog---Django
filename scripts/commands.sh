#!/bin/sh

# O commands.sh garante que o banco esteja pronto, 
# aplica as configurações do Django e roda o servidor.

# define que é um script shell, e se der problema deve parar
set -e

# shell script que espera o postgres ficar diponível antes do continuar, para não dar erros

wait_psql.sh
# coleta os arquivos estaticos
collectstatic.sh
# criando as migrações, antes de migar de fato
# Aplica as migrações no banco de dados
migrate.sh
# roda o server
runserver.sh