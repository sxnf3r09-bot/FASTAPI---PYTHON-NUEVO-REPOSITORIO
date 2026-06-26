from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel, Field

# Nota: Mantener los modelos de simulación actuales activos mientras el instructor 
# migra cada entidad a tablas de SQLModel en las siguientes clases.

# =====================================================================
# MODELOS DE PYDANTIC: CLIENTES
# =====================================================================

class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    descripcion: Optional[str] = None

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True


# =====================================================================
# MODELOS DE PYDANTIC: TRANSACCIONES
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


# =====================================================================
# MODELOS DE PYDANTIC: FACTURAS
# =====================================================================

class FacturaBase(BaseModel):
    monto_total: float
    estado: str = "Pendiente"

class FacturaCrear(FacturaBase):
    pass

class FacturaResponse(FacturaBase):
    id: int
    id_cliente: int

    class Config:
        from_attributes = True