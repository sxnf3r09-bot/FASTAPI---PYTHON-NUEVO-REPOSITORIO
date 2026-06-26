from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from modelos import Factura, FacturaCrear, Cliente, FacturaConTransacciones
from conexion_bd import obtener_sesion

ratas_facturas = APIRouter()

@ratas_facturas.post("/facturas", response_model=Factura, status_code=status.HTTP_201_CREATED)
async def crear_factura(datos_factura: FacturaCrear, sesion: Session = Depends(obtener_sesion)):
    cliente = sesion.get(Cliente, datos_factura.cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El cliente no existe."
        )
    
    nueva_factura = Factura.model_validate(datos_factura)
    sesion.add(nueva_factura)
    sesion.commit()
    sesion.refresh(nueva_factura)
    return nueva_factura

@ratas_facturas.get("/facturas", response_model=list[FacturaConTransacciones])
async def listar_facturas(sesion: Session = Depends(obtener_sesion)):
    facturas = sesion.exec(select(Factura)).all()
    return facturas