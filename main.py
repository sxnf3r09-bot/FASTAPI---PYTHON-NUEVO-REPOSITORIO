from fastapi import FastAPI

app = FastAPI()

# Lista de diccionarios que actúa como base de datos simulada de clientes
lista_clientes = [
    {"cliente_id": 1, "nombre": "Santiago Fernandez", "ciudad": "Bogota"},
    {"cliente_id": 2, "nombre": "Jhonny Guerrero", "ciudad": "Medellin"},
    {"cliente_id": 3, "nombre": "Carlos Mendoza", "ciudad": "Cali"}
]

@app.get("/")
def inicio():
    return {"mensaje": "hola estoy aprendiendo FAS App"}

# Endpoint para listar TODOS los clientes
@app.get("/clientes")
def listar_clientes():
    return lista_clientes

# Endpoint para listar UN SOLO cliente por su cliente_id
@app.get("/clientes/{cliente_id}")
def listar_cliente_id(cliente_id: int):
    # Recorremos la lista de clientes para buscar la coincidencia
    for cliente in lista_clientes:
        if cliente["cliente_id"] == cliente_id:
            return cliente
    # Si no lo encuentra, retorna un mensaje de error
    return {"error": "Cliente no encontrado"}