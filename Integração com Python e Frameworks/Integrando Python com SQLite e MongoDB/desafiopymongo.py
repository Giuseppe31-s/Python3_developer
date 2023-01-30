import datetime
import pprint

import pymongo
import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://<user>:<senha>@cluster0.yusqfdt.mongodb.net/?retryWrites=true&w=majority")

db = client["bank"]
collection = db["clientes"]

cliente = {
    "nome": "Juliana",
    "cpf": "123456789",
    "endereco": "San Martin",
    "contas": [
        {"tipo": "corrente", "numero": "001", "saldo": 1000.0},
        {"tipo": "poupança", "numero": "002", "saldo": 2000.0}
    ]
}

collection.insert_one(cliente)

# Recuperar todos os clientes
clientes = list(collection.find({}))

joao = {
    "nome": "João",
    "cpf": "987654321",
    "endereco": "Rua dos Bobos",
    "contas": [
    {"tipo": "corrente", "numero": "003", "saldo": 1500.0}]
}

maria = {
    "nome": "Maria",
    "cpf": "2468101214",
    "endereco": "Avenida Paulista",
    "contas": [
    {"tipo": "corrente", "numero": "005", "saldo": 1700.0}]
}

clientes_novo = [joao, maria]
collection.insert_many(clientes_novo)

# Nomes que começam com a letra "J"
filtro = {"nome": {"$regex": "^J"}}

clientes_filtrados = list(collection.find(filtro))

for cliente in clientes_filtrados:
    pprint.pprint(cliente)