from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# =====================================================================
# TABLA REAL: CLIENTES
# =====================================================================
class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    descripcion: Optional[str] = None
    
    # Relación virtual: Un cliente puede tener muchas facturas
    facturas: List["Factura"] = Relationship(back_populates="cliente")

class ClienteCrear(BaseModel):
    nombre: str
    email: EmailStr
    descripcion: Optional[str] = None

class ClienteEditar(BaseModel):
    nombre: str
    email: EmailStr
    descripcion: Optional[str] = None


# =====================================================================
# TABLA REAL: FACTURAS
# =====================================================================
class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto_total: float
    estado: str = Field(default="Pendiente")
    cliente_id: int = Field(foreign_key="cliente.id")
    
    # Relaciones virtuales de Factura
    cliente: Optional[Cliente] = Relationship(back_populates="facturas")
    transacciones: List["Transaccion"] = Relationship(back_populates="factura")

    # Propiedad calculada (@property) explicada en el video para sumar montos si se requiere
    @property
    def total_pagado(self) -> float:
        return sum(t.monto for t in self.transacciones if t.tipo.lower() == "pago")

class FacturaCrear(BaseModel):
    monto_total: float
    cliente_id: int
    estado: Optional[str] = "Pendiente"


# =====================================================================
# TABLA REAL: TRANSACCIONES
# =====================================================================
class Transaccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto: float
    tipo: str
    id_factura: int = Field(foreign_key="factura.id")
    
    # Relación virtual: Una transacción pertenece a una factura
    factura: Optional[Factura] = Relationship(back_populates="transacciones")

class TransaccionCrear(BaseModel):
    monto: float
    tipo: str
    id_factura: int