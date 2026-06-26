from sqlmodel import SQLModel, create_engine, Session

nombre_base_datos = "base_datos.db"
url_base_datos = f"sqlite:///{nombre_base_datos}"

# El argumento connect_args es necesario solo para SQLite
motor = create_engine(url_base_datos, connect_args={"check_same_thread": False})

def crear_tablas_bd():
    SQLModel.metadata.create_all(motor)

def obtener_sesion():
    with Session(motor) as sesion:
        yield sesion    