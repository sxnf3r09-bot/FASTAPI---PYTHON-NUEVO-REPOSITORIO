from fastapi import APIRouter, HTTPException
from modelos import ClienteCrear, ClienteEditar

ratas_clientes = APIRouter()

lista_clientes = [
    {"id": 1, "nombre": "Santiago Fernandez", "email": "santiago@sena.edu.co", "descripcion": "Vocero de la ficha"},
    {"id": 2, "nombre": "Jhonny Guerrero", "email": "jhonny@sena.edu.co", "descripcion": "Instructor principal"},
]

@ratas_clientes.get("/clientes")
async def listar_clientes():
    return lista_clientes

@ratas_clientes.get("/clientes/{cliente_id}")
async def listar_cliente_id(cliente_id: int):
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            return cliente
    raise HTTPException(status_code=404, detail=f"El cliente con id {cliente_id}, no existe.")

@ratas_clientes.post("/clientes")
async def crear_cliente(datos_cliente: ClienteCrear):
    nuevo_id = lista_clientes[-1]["id"] + 1 if lista_clientes else 1
    cliente_dict = datos_cliente.model_dump()
    cliente_dict["id"] = nuevo_id
    lista_clientes.append(cliente_dict)
    return {"mensaje": "Cliente creado exitosamente", "cliente": cliente_dict}

@ratas_clientes.put("/clientes/{cliente_id}")
async def editar_cliente(cliente_id: int, datos_actualizados: ClienteEditar):
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            cliente["nombre"] = datos_actualizados.nombre
            cliente["email"] = datos_actualizados.email
            cliente["descripcion"] = datos_actualizados.descripcion
            return {"mensaje": "Cliente modificado exitosamente", "cliente": cliente}
    raise HTTPException(status_code=404, detail="Cliente no encontrado para editar")

@ratas_clientes.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int):
    for indice, cliente in enumerate(lista_clientes):
        if cliente["id"] == cliente_id:
            cliente_eliminado = lista_clientes.pop(indice)
            return {"mensaje": "Cliente eliminado exitosamente", "cliente": cliente_eliminado}
    raise HTTPException(status_code=404, detail="Cliente no encontrado para eliminar")