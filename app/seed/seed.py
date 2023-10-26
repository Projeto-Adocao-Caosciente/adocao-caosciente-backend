import bson
from pymongo import MongoClient

# TODO: Pegar das variávies de ambiente
DB_URL = "" 
DB_NAME = ""

client = MongoClient(DB_URL)
db = client.get_database(DB_NAME)
session = client.start_session()

ongs_collection = db.get_collection("ongs")
animals_collection = db.get_collection("animals")

sample_ong = {
    "cnpj": "12345678901234",
    "name": "ONG Teste",
    "logo": "https://unsplash.it/500/500",
    "city": "São Paulo",
    "state": "SP",
    "phone": "11999999999",
    "email": "nome@email.com.br",
    "mission": "Missão exemplo",
    "foundation": "01-01-2021T00:00:00Z",
    "description": "Descrição exemplo",
    "animals": [],
    "password": "senha123",
}

ongs_collection.insert_one(sample_ong)

# Read a json at same folder in python
import json

with open('animals.json') as f:
    data = json.load(f)
    animals_ids = animals_collection.insert_many(data).inserted_ids
    ong = ongs_collection.find_one({"cnpj": "12345678901234"})
    ongs_collection.update_one(
        {"_id": ong["_id"]},
        {"$push": {"animals": {"$each": animals_ids}}}
    )

print("Done!")