from fastapi import FastAPI
from enrutadores.clientes import ratas_clientes
from enrutadores.transacciones import ratas_transacciones
from enrutadores.facturas import ratas_facturas
from conexion_bd import crear_tablas_bd

app = FastAPI()

@app.on_event("startup")
def al_iniciar():
    crear_tablas_bd()

# Registro de todos los enrutadores del proyecto
app.include_router(ratas_clientes)
app.include_router(ratas_transacciones)
app.include_router(ratas_facturas)

@app.get("/")
def inicio():
    return {"mensaje": "hola estoy aprendiendo FAS App, con Tablas Relacionales!"}