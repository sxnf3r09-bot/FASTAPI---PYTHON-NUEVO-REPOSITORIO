from pydantic import BaseModel

# Clase base que define cómo luce un Cliente de manera general
class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str

# Clase que hereda de ClienteBase para la creación de nuevos registros
class ClienteCrear(ClienteBase):
    pass