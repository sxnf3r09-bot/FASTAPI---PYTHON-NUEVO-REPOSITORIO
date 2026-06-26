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
# TABLA REAL: FACTURAS
# =====================================================================
class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto_total: float
    estado: str = Field(default="Pendiente")
    cliente_id: int = Field(foreign_key="cliente.id")

class FacturaCrear(BaseModel):
    monto_total: float
    cliente_id: int
    estado: Optional[str] = "Pendiente"


# =====================================================================
# TABLA REAL: TRANSACCIONES (NUEVA MIGRACIÓN)
# =====================================================================
class Transaccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto: float
    tipo: str  # Ejemplo: "Pago", "Reembolso"
    
    # Llave foránea vinculada directamente a la tabla factura
    id_factura: int = Field(foreign_key="factura.id")

class TransaccionCrear(BaseModel):
    monto: float
    tipo: str
    id_factura: int