from fastapi import FastAPI
from enrutadores.clientes import ratas_clientes
from enrutadores.transacciones import ratas_transacciones

app = FastAPI()

# Registro de enrutadores globales
app.include_router(ratas_clientes)
app.include_router(ratas_transacciones)

@app.get("/")
def inicio():
    return {"mensaje": "hola estoy aprendiendo FAS App, ahora estructurado!"}