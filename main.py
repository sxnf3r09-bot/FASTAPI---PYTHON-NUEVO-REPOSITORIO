from fastapi import FastAPI
from enrutadores.clientes import ratas_clientes

app = FastAPI()

app.include_router(ratas_clientes)

@app.get("/")
def inicio():
    return {"mensaje": "hola estoy aprendiendo FAS App, ahora estructurado!"}