from fastapi import FastAPI, HTTPException
# Importamos los esquemas desde nuestro archivo de modelos
from modelos import ClienteCrear

app = FastAPI()

# Lista de simulación (Base de datos temporal)
lista_clientes = [
    {"id": 1, "nombre": "Santiago Fernandez", "email": "santiago@sena.edu.co", "descripcion": "Vocero de la ficha"},
    {"id": 2, "nombre": "Jhonny Guerrero", "email": "jhonny@sena.edu.co", "descripcion": "Instructor principal"},
]

@app.get("/")
def inicio():
    return {"mensaje": "hola estoy aprendiendo FAS App"}

# Endpoint para listar todos los clientes
@app.get("/clientes")
def listar_clientes():
    return lista_clientes

# Endpoint para registrar un nuevo cliente usando el modelo de Pydantic
@app.post("/clientes")
def crear_cliente(datos_cliente: ClienteCrear):
    # Generamos un ID simulado sumando 1 al último elemento
    nuevo_id = lista_clientes[-1]["id"] + 1 if lista_clientes else 1
    
    # Convertimos el modelo de Pydantic a un diccionario de Python
    cliente_dict = datos_cliente.model_dump()
    cliente_dict["id"] = nuevo_id
    
    # Guardamos en nuestra lista
    lista_clientes.append(cliente_dict)
    return {"mensaje": "Cliente creado exitosamente", "cliente": cliente_dict}