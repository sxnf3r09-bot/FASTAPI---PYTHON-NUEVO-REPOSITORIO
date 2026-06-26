from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from modelos import Factura, FacturaCrear, Cliente
from conexion_bd import obtener_sesion

ratas_facturas = APIRouter()

# 1. CREAR UNA FACTURA VALIDANDO QUE EL CLIENTE EXISTA
@ratas_facturas.post("/facturas", response_model=Factura, status_code=status.HTTP_201_CREATED)
async def crear_factura(datos_factura: FacturaCrear, sesion: Session = Depends(obtener_sesion)):
    # Validar primero si el cliente existe en la base de datos
    cliente = sesion.get(Cliente, datos_factura.cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear la factura. El cliente con id {datos_factura.cliente_id} no existe."
        )
    
    # Mapear los datos de validación al modelo de la tabla real
    nueva_factura = Factura.model_validate(datos_factura)
    sesion.add(nueva_factura)
    sesion.commit()
    sesion.refresh(nueva_factura)
    return nueva_factura

# 2. LISTAR TODAS LAS FACTURAS DESDE LA BASE DE DATOS
@ratas_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas(sesion: Session = Depends(obtener_sesion)):
    facturas = sesion.exec(select(Factura)).all()
    return facturas