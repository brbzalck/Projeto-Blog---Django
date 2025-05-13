# O Dockerfile prepara o ambiente com Python, dependências, diretórios e permissões.


# criando a imagem docker com python baseada em Alpine Linux
FROM python:3.11.3-alpine3.18
# mostra quem mantêm esse dockerfile
LABEL mantainer="https://github.com/brbzalck"

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "djangoapp" e "scripts" para dentro do container.
COPY djangoapp /djangoapp
COPY scripts /scripts

# Definindo diretório principal de comandos pelo docker
WORKDIR /djangoapp

# A porta 8000 estará disponível para conexões externas ao container
# É a porta que vamos usar para o Django.
EXPOSE 8000

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.

# criando ambiente virtual na raiz do projeto
RUN python -m venv /venv && \
    # atualizando pip
  /venv/bin/pip install --upgrade pip && \
    # pegando os requerimentos do projeto
  /venv/bin/pip install -r /djangoapp/requirements.txt && \
    # adicionando um usuário, sem senha e sem home, de nome duser
  adduser --disabled-password --no-create-home duser && \
    # criando a pasta static
  mkdir -p /data/web/static && \
    # criando a pasta media
  mkdir -p /data/web/media/assets/favicon && \
  mkdir -p /data/web/media/posts && \
    # modificando quem criou as pastas venv, static e media
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
    # mudando a permissão das pastas para 755
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
    # +x para executar somento com o nome do arquivo
  chmod -R +x /scripts

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Muda o usuário para duser
USER duser

# Executa o arquivo scripts/commands.sh
CMD ["/scripts/commands.sh"]