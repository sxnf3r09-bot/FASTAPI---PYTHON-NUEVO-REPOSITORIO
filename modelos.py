from pydantic import BaseModel

# Clase base con los campos comunes
class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str

# Clase para la creación de nuevos registros
class ClienteCrear(ClienteBase):
    pass

# Clase para la actualización/edición de registros existentes
class ClienteEditar(ClienteBase):
    pass

from pydantic import BaseModel

# --- MODELOS DE CLIENTES (Clases anteriores) ---
class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass


# --- MODELOS DE TRANSACCIONES (Clase 7) ---
class TransaccionBase(BaseModel):
    id_factura: int
    monto: float
    descripcion: str

class TransaccionCrear(TransaccionBase):
    pass

class TransaccionResponse(TransaccionBase):
    id: int

    from pydantic import BaseModel

# ... (Mantén tus clases anteriores de Clientes y Transacciones intactas) ...

# --- MODELOS DE FACTURAS (Clase 8) ---
class FacturaBase(BaseModel):
    id_cliente: int
    monto_total: float
    estado: str  # Ejemplo: "Pagada", "Pendiente"

class FacturaCrear(FacturaBase):
    pass

class FacturaResponse(FacturaBase):
    id: int