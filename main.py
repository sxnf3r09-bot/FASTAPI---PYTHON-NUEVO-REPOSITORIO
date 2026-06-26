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

from fastapi import FastAPI, HTTPException
from modelos import ClienteCrear, ClienteEditar
# Importamos los nuevos modelos de transacciones
from modelos import TransaccionCrear, TransaccionResponse

app = FastAPI()

# ... (Aquí se mantiene intacto todo tu código anterior de Clientes) ...

# =====================================================================
# RUTAS DE TRANSACCIONES - CLASE 7 (ENDPOINTS VACÍOS)
# =====================================================================

# 1. Listar todas las transacciones
@app.get("/transacciones", response_model=list[TransaccionResponse])
def listar_transacciones():
    pass

# 2. Listar una sola transacción por su ID
@app.get("/transacciones/{transaccion_id}", response_model=TransaccionResponse)
def listar_transaccion_id(transaccion_id: int):
    pass

# 3. Filtrar transacciones por el ID de una factura
@app.get("/transacciones/factura/{id_factura}", response_model=list[TransaccionResponse])
def listar_transacciones_factura(id_factura: int):
    pass

# 4. Crear una nueva transacción
@app.post("/transacciones", response_model=TransaccionResponse)
def crear_transaccion(transaccion: TransaccionCrear):
    pass

# 5. Eliminar una transacción
@app.delete("/transacciones/{transaccion_id}", response_model=TransaccionResponse)
def eliminar_transaccion(transaccion_id: int):
    pass

from fastapi import FastAPI, HTTPException
from modelos import ClienteCrear, ClienteEditar
from modelos import TransaccionCrear, TransaccionResponse
# Importamos los nuevos modelos de facturas
from modelos import FacturaCrear, FacturaResponse

app = FastAPI()

# ... (Aquí se mantiene todo tu código anterior de Clientes y Transacciones) ...

# =====================================================================
# ENTIDAD FACTURAS - CLASE 8 (CON LÓGICA Y VALIDACIÓN)
# =====================================================================

# Lista de simulación para base de datos de facturas
lista_facturas = [
    {"id": 1, "id_cliente": 1, "monto_total": 150000.0, "estado": "Pendiente"},
    {"id": 2, "id_cliente": 1, "monto_total": 320000.0, "estado": "Pagada"},
]

# 1. Listar todas las facturas
@app.get("/facturas", response_model=list[FacturaResponse])
def listar_facturas():
    return lista_facturas

# 2. Listar una sola factura por su ID (Lógica principal del Video #8)
@app.get("/facturas/{factura_id}", response_model=FacturaResponse)
def obtener_factura_id(factura_id: int):
    for factura in lista_facturas:
        if factura["id"] == factura_id:
            return factura
            
    # Si termina el ciclo y no la encuentra, dispara el error 404
    raise HTTPException(status_code=404, detail="Factura no encontrada")