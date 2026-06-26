from fastapi import FastAPI, HTTPException
from modelos import ClienteCrear, ClienteEditar

app = FastAPI()

# Lista de simulación (Base de datos temporal)
lista_clientes = [
    {"id": 1, "nombre": "Santiago Fernandez", "email": "santiago@sena.edu.co", "descripcion": "Vocero de la ficha"},
    {"id": 2, "nombre": "Jhonny Guerrero", "email": "jhonny@sena.edu.co", "descripcion": "Instructor principal"},
]

@app.get("/")
def inicio():
    return {"mensaje": "hola estoy aprendiendo FAS App"}

# 1. LEER TODOS (GET)
@app.get("/clientes")
def listar_clientes():
    return lista_clientes

# 2. LEER UNO SOLO (GET por ID)
@app.get("/clientes/{cliente_id}")
def listar_cliente_id(cliente_id: int):
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# 3. CREAR (POST)
@app.post("/clientes")
def crear_cliente(datos_cliente: ClienteCrear):
    nuevo_id = lista_clientes[-1]["id"] + 1 if lista_clientes else 1
    cliente_dict = datos_cliente.model_dump()
    cliente_dict["id"] = nuevo_id
    lista_clientes.append(cliente_dict)
    return {"mensaje": "Cliente creado exitosamente", "cliente": cliente_dict}

# 4. EDITAR (PUT) - Implementado en la Clase 6
@app.put("/clientes/{cliente_id}")
def editar_cliente(cliente_id: int, datos_actualizados: ClienteEditar):
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            # Actualizamos los campos con los nuevos datos validados por Pydantic
            cliente["nombre"] = datos_actualizados.nombre
            cliente["email"] = datos_actualizados.email
            cliente["descripcion"] = datos_actualizados.descripcion
            return {"mensaje": "Cliente modificado exitosamente", "cliente": cliente}
            
    raise HTTPException(status_code=404, detail="Cliente no encontrado para editar")

# 5. ELIMINAR (DELETE) - Ejercicio del CRUD completo
@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    for indice, cliente in enumerate(lista_clientes):
        if cliente["id"] == cliente_id:
            # Eliminamos el cliente de la lista usando su índice
            cliente_eliminado = lista_clientes.pop(indice)
            return {"mensaje": "Cliente eliminado exitosamente", "cliente": cliente_eliminado}
            
    raise HTTPException(status_code=404, detail="Cliente no encontrado para eliminar")