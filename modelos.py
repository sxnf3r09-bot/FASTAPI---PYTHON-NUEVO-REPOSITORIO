from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# =====================================================================
# MODELOS BASE (Para evitar herencias cruzadas)
# =====================================================================
class ClienteBase(SQLModel):
    nombre: str
    email: str
    descripcion: Optional[str] = None

class FacturaBase(SQLModel):
    monto_total: float
    estado: str = "Pendiente"
    cliente_id: int

class TransaccionBase(SQLModel):
    monto: float
    tipo: str
    id_factura: int

# =====================================================================
# TABLAS REALES EN BASE DE DATOS
# =====================================================================
class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    facturas: List["Factura"] = Relationship(back_populates="cliente")

class Factura(FacturaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    
    cliente: Optional[Cliente] = Relationship(back_populates="facturas")
    transacciones: List["Transaccion"] = Relationship(back_populates="factura")

class Transaccion(TransaccionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_factura: int = Field(foreign_key="factura.id")
    
    factura: Optional[Factura] = Relationship(back_populates="transacciones")

# =====================================================================
# ESQUEMAS DE PETICIÓN (DTOs / VALIDACIÓN)
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
# ESQUEMAS DE RESPUESTA ANIDADOS (La magia del Video 21)
# =====================================================================
class TransaccionResponse(TransaccionBase):
    id: int

class FacturaConTransacciones(FacturaBase):
    id: int
    transacciones: List[TransaccionResponse] = []

class ClienteConFacturas(ClienteBase):
    id: int
    facturas: List[FacturaConTransacciones] = []