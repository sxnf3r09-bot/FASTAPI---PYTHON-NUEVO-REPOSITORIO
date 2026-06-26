from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from modelos import Cliente, ClienteCrear, ClienteEditar
from conexion_bd import obtener_sesion

ratas_clientes = APIRouter()

# Endpoint para listar todos los clientes desde la base de datos real
@ratas_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes(sesion: Session = Depends(obtener_sesion)):
    clientes = sesion.exec(select(Cliente)).all()
    return clientes

# Endpoint para obtener un solo cliente de la base de datos
@ratas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente_id(cliente_id: int, sesion: Session = Depends(obtener_sesion)):
    cliente = sesion.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail=f"El cliente con id {cliente_id}, no existe.")
    return cliente

# Endpoint para crear un cliente guardándolo directamente en SQLite
@ratas_clientes.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear, sesion: Session = Depends(obtener_sesion)):
    nuevo_cliente = Cliente.model_validate(datos_cliente)
    sesion.add(nuevo_cliente)
    sesion.commit()
    sesion.refresh(nuevo_cliente)
    return nuevo_cliente

@ratas_clientes.put("/clientes/{cliente_id}")
async def editar_cliente(cliente_id: int, datos_actualizados: ClienteEditar):
    # Nota: Este se mantendrá temporal hasta que el instructor muestre la edición en la BD
    raise HTTPException(status_code=501, detail="Endpoint en mantenimiento para migración a BD")

@ratas_clientes.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int):
    # Nota: Este se mantendrá temporal hasta que el instructor muestre la eliminación en la BD
    raise HTTPException(status_code=501, detail="Endpoint en mantenimiento para migración a BD")