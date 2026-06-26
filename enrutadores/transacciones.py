from fastapi import APIRouter, HTTPException
from modelos import TransaccionCrear, TransaccionResponse

ratas_transacciones = APIRouter()

# Lista de simulación global para transacciones
lista_transacciones = []

@ratas_transacciones.get("/transacciones", response_model=list[TransaccionResponse])
async def listar_transacciones():
    return lista_transacciones

@ratas_transacciones.get("/transacciones/{transaccion_id}", response_model=TransaccionResponse)
async def listar_transaccion_id(transaccion_id: int):
    for transaccion in lista_transacciones:
        if transaccion["id"] == transaccion_id:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@ratas_transacciones.post("/transacciones", response_model=TransaccionResponse)
async def crear_transaccion(transaccion: TransaccionCrear):
    nuevo_id = lista_transacciones[-1]["id"] + 1 if lista_transacciones else 1
    transaccion_dict = transaccion.model_dump()
    transaccion_dict["id"] = nuevo_id
    lista_transacciones.append(transaccion_dict)
    return transaccion_dict

@ratas_transacciones.delete("/transacciones/{transaccion_id}", response_model=TransaccionResponse)
async def eliminar_transaccion(transaccion_id: int):
    for indice, transaccion in enumerate(lista_transacciones):
        if transaccion["id"] == transaccion_id:
            return lista_transacciones.pop(indice)
    raise HTTPException(status_code=404, detail="Transacción no encontrada para eliminar")