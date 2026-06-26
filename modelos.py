from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# =====================================================================
# TABLAS REALES EN BASE DE DATOS (Mapeo directo a SQLite)
# =====================================================================

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    descripcion: Optional[str] = None
    
    # Relación virtual inversa hacia Facturas
    facturas: List[Factura] = Relationship(back_populates="cliente")


class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto_total: float
    estado: str = Field(default="Pendiente")
    
    # Llave foránea hacia Cliente
    cliente_id: int = Field(foreign_key="cliente.id")
    
    # Relaciones virtuales
    cliente: Optional[Cliente] = Relationship(back_populates="facturas")
    transacciones: List[Transaccion] = Relationship(back_populates="factura")


class Transaccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto: float
    tipo: str
    
    # Llave foránea hacia Factura
    id_factura: int = Field(foreign_key="factura.id")
    
    # Relación virtual
    factura: Optional[Factura] = Relationship(back_populates="transacciones")


# =====================================================================
# ESQUEMAS DE PETICIÓN (DTOs / Validación de entrada)
# =====================================================================

class ClienteCrear(BaseModel):
    nombre: str
    email: EmailStr
    descripcion: Optional[str] = None

class ClienteEditar(BaseModel):
    nombre: str
    email: EmailStr
    descripcion: Optional[str] = None

class FacturaCrear(BaseModel):
    monto_total: float
    cliente_id: int
    estado: Optional[str] = "Pendiente"

class TransaccionCrear(BaseModel):
    monto: float
    tipo: str
    id_factura: int


# =====================================================================
# ESQUEMAS DE RESPUESTA ANIDADOS (Serialización limpia)
# =====================================================================

class TransaccionResponse(BaseModel):
    id: int
    monto: float
    tipo: str
    id_factura: int

class FacturaConTransacciones(BaseModel):
    id: int
    monto_total: float
    estado: str
    cliente_id: int
    transacciones: List[TransaccionResponse] = []

class ClienteConFacturas(BaseModel):
    id: int
    nombre: str
    email: str
    descripcion: Optional[str] = None
    facturas: List[FacturaConTransacciones] = []