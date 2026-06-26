from pydantic import BaseModel, EmailStr
from typing import Optional

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