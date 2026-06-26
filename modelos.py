from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel, Field

# =====================================================================
# TABLA REAL: CLIENTES
# =====================================================================
class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    descripcion: Optional[str] = None

class ClienteCrear(BaseModel):
    nombre: str
    email: EmailStr
    descripcion: Optional[str] = None

class ClienteEditar(BaseModel):
    nombre: str
    email: EmailStr
    descripcion: Optional[str] = None


# =====================================================================
# TABLA REAL: FACTURAS (NUEVA RELACIÓN)
# =====================================================================
class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto_total: float
    estado: str = Field(default="Pendiente")
    
    # Llave foránea que conecta la factura con un cliente existente
    cliente_id: int = Field(foreign_key="cliente.id")

class FacturaCrear(BaseModel):
    monto_total: float
    cliente_id: int
    estado: Optional[str] = "Pendiente"


# =====================================================================
# MODELOS TEMPORALES DE SIMULACIÓN (Transacciones se migrarán después)
# =====================================================================
class TransaccionBase(BaseModel):
    id_factura: int
    monto: float
    tipo: str

class TransaccionCrear(TransaccionBase):
    pass

class TransaccionResponse(TransaccionBase):
    id: int

    class Config:
        from_attributes = True