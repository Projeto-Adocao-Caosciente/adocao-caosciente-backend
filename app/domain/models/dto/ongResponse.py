from typing import Annotated
from pydantic import WithJsonSchema

from app.domain.models.ong import OngModel

# TODO: Criar responses padrões para todas as rotas como forma de documentação

CreateOng = Annotated[None, WithJsonSchema(json_schema={"message": "Ong created successfully.", "data": None})]