from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from modelos import Cliente, ClienteCrear, ClienteEditar, ClienteConFacturas
from conexion_bd import obtener_sesion

ratas_clientes = APIRouter()

@ratas_clientes.get("/clientes", response_model=list[ClienteConFacturas])
async def listar_clientes(sesion: Session = Depends(obtener_sesion)):
    clientes = sesion.exec(select(Cliente)).all()
    return clientes

@ratas_clientes.get("/clientes/{cliente_id}", response_model=ClienteConFacturas)
async def listar_cliente_id(cliente_id: int, sesion: Session = Depends(obtener_sesion)):
    cliente = sesion.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@ratas_clientes.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def crear_cliente(datos_cliente: ClienteCrear, sesion: Session = Depends(obtener_sesion)):
    nuevo_cliente = Cliente.model_validate(datos_cliente)
    sesion.add(nuevo_cliente)
    sesion.commit()
    sesion.refresh(nuevo_cliente)
    return nuevo_cliente