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

ENVIRONMENT=development

DATABASE_URL_TEST=mongodb://localhost:27017/
DATABASE_NAME_TEST=adocaosciente_test_db
```

estas, devem ser substituidas pelos valores de conexão com o banco de dados **mongodb**.

## Execução dos testes

Para executar os testes, antes de tudo, é necessário ter o banco de dados mongodb rodando na porta padrão (27017).

para isso execute o comando ```docker-compose up -d``` na raiz do projeto.

após isso, verifique se a variavel de ambiente `ENVIRONMENT` está com o valor `test` no arquivo `.env`. Caso não esteja, altere o valor para `test`.

por fim, execute o comando ```python -m pytest ``` na raiz do projeto.

## Execução do projeto

1. No linux rode o comando ```poetry run ./entrypoint.sh```. No Windows o comando é ```uvicorn app.main:api --host 0.0.0.0 --reload --log-level=trace```
2. Acesse o documento de swagger através do link ```http://localhost:8000/docs```
