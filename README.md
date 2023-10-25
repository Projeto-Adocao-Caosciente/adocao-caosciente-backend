# Intruções de Intalação

## Pré-requisitos

- Tenha Python3 instalado

## Instalação via poetry

- Instale [poetry](https://python-poetry.org/docs/), recomendamos utilizar o pip.
- Rode o comando ```poetry install``` na pasta do projeto

## Instalação sem poetry

- Instale todas as depedências com a execução do comando ```pip install -r requirements.txt``` na raiz do projeto

## Configurando variáveis de ambiente

Crie um arquivo chamado `.env` na pasta raiz do projeto, dentro dele coloque as seguintes variáveis de ambiente:

```text
DATABASE_URL=
DATABASE_NAME=
```

estas, devem ser substituidas pelos valores de conexão com o banco de dados **mongodb**.

Caso esteja usando docker substitua pelo nome definido em seu **docker-compose.yml*

## Execução do projeto

1. No linux rode o comando ```poetry run ./entrypoint.sh```. No Windows o comando é ```uvicorn app.main:api --host 0.0.0.0 --reload --log-level=trace```
2. Acesse o documento de swagger através do link ```http://localhost:8000/docs```
