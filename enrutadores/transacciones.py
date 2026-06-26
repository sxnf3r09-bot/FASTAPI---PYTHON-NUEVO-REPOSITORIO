from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from modelos import Transaccion, TransaccionCrear, Factura
from conexion_bd import obtener_sesion

ratas_transacciones = APIRouter()

# 1. CREAR TRANSACCIÓN VALIDANDO QUE LA FACTURA EXISTA
@ratas_transacciones.post("/transacciones", response_model=Transaccion, status_code=status.HTTP_201_CREATED)
async def crear_transaccion(datos_transaccion: TransaccionCrear, sesion: Session = Depends(obtener_sesion)):
    # Validar que la factura relacionada exista en la BD
    factura = sesion.get(Factura, datos_transaccion.id_factura)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede registrar la transacción. La factura con id {datos_transaccion.id_factura} no existe."
        )
    
    nueva_transaccion = Transaccion.model_validate(datos_transaccion)
    sesion.add(nueva_transaccion)
    sesion.commit()
    sesion.refresh(nueva_transaccion)
    return nueva_transaccion

# 2. LISTAR TODAS LAS TRANSACCIONES DESDE LA BASE DE DATOS
@ratas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones(sesion: Session = Depends(obtener_sesion)):
    transacciones = sesion.exec(select(Transaccion)).all()
    return transacciones

# 3. OBTENER UNA TRANSACCIÓN POR ID
@ratas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def listar_transaccion_id(transaccion_id: int, sesion: Session = Depends(obtener_sesion)):
    transaccion = sesion.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Transacción no encontrada"
        )
    return transaccion