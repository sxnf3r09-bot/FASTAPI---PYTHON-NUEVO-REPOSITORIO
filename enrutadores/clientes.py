from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from modelos import Cliente, ClienteCrear, ClienteEditar
from conexion_bd import obtener_sesion

ratas_clientes = APIRouter()

# 1. LISTAR TODOS LOS CLIENTES
@ratas_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes(sesion: Session = Depends(obtener_sesion)):
    clientes = sesion.exec(select(Cliente)).all()
    return clientes

# 2. OBTENER UN CLIENTE POR ID
@ratas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente_id(cliente_id: int, sesion: Session = Depends(obtener_sesion)):
    cliente = sesion.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"El cliente con id {cliente_id}, no existe."
        )
    return cliente

# 3. CREAR UN NUEVO CLIENTE
@ratas_clientes.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def crear_cliente(datos_cliente: ClienteCrear, sesion: Session = Depends(obtener_sesion)):
    nuevo_cliente = Cliente.model_validate(datos_cliente)
    sesion.add(nuevo_cliente)
    sesion.commit()
    sesion.refresh(nuevo_cliente)
    return nuevo_cliente

# 4. EDITAR / ACTUALIZAR UN CLIENTE EXISTENTE
@ratas_clientes.put("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_actualizados: ClienteEditar, sesion: Session = Depends(obtener_sesion)):
    cliente_bd = sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"El cliente con id {cliente_id}, no existe para editar."
        )
    
    # Extraer los datos enviados y actualizar los campos del objeto de la BD
    datos_dict = datos_actualizados.model_dump(exclude_unset=True)
    for clave, valor in datos_dict.items():
        setattr(cliente_bd, clave, valor)
        
    sesion.add(cliente_bd)
    sesion.commit()
    sesion.refresh(cliente_bd)
    return cliente_bd

# 5. ELIMINAR UN CLIENTE
@ratas_clientes.delete("/clientes/{cliente_id}", response_model=dict)
async def eliminar_cliente(cliente_id: int, sesion: Session = Depends(obtener_sesion)):
    cliente_bd = sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"El cliente con id {cliente_id}, no existe para eliminar."
        )
    
    sesion.delete(cliente_bd)
    sesion.commit()
    return {"mensaje": "Cliente eliminado exitosamente", "id_eliminado": cliente_id}