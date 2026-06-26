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