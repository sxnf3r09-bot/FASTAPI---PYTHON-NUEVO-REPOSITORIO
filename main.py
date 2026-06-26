from fastapi import FastAPI, HTTPException, status
from modelos import (
    ClienteCrear, 
    ClienteEditar, 
    TransaccionCrear, 
    TransaccionResponse, 
    FacturaCrear, 
    FacturaResponse
)

app = FastAPI()

# =====================================================================
# DATA STORAGE (SIMULACIÓN DE BASE DE DATOS)
# =====================================================================
lista_clientes = [
    {"id": 1, "nombre": "Santiago Fernandez", "email": "santiago@sena.edu.co", "descripcion": "Vocero de la ficha"},
    {"id": 2, "nombre": "Jhonny Guerrero", "email": "jhonny@sena.edu.co", "descripcion": "Instructor principal"},
]

lista_facturas = [
    {"id": 1, "id_cliente": 1, "monto_total": 150000.0, "estado": "Pendiente"},
    {"id": 2, "id_cliente": 1, "monto_total": 320000.0, "estado": "Pagada"},
]

lista_transacciones = []


@app.get("/")
def inicio():
    return {"mensaje": "hola estoy aprendiendo FAS App"}

# =====================================================================
# ENDPOINTS: ENTIDAD CLIENTES
# =====================================================================

@app.get("/clientes")
def listar_clientes():
    return lista_clientes

@app.get("/clientes/{cliente_id}")
def listar_cliente_id(cliente_id: int):
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.post("/clientes")
def crear_cliente(datos_cliente: ClienteCrear):
    nuevo_id = lista_clientes[-1]["id"] + 1 if lista_clientes else 1
    cliente_dict = datos_cliente.model_dump()
    cliente_dict["id"] = nuevo_id
    lista_clientes.append(cliente_dict)
    return {"mensaje": "Cliente creado exitosamente", "cliente": cliente_dict}

@app.put("/clientes/{cliente_id}")
def editar_cliente(cliente_id: int, datos_actualizados: ClienteEditar):
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            cliente["nombre"] = datos_actualizados.nombre
            cliente["email"] = datos_actualizados.email
            cliente["descripcion"] = datos_actualizados.descripcion
            return {"mensaje": "Cliente modificado exitosamente", "cliente": cliente}
    raise HTTPException(status_code=404, detail="Cliente no encontrado para editar")

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    for indice, cliente in enumerate(lista_clientes):
        if cliente["id"] == cliente_id:
            cliente_eliminado = lista_clientes.pop(indice)
            return {"mensaje": "Cliente eliminado exitosamente", "cliente": cliente_eliminado}
    raise HTTPException(status_code=404, detail="Cliente no encontrado para eliminar")


# =====================================================================
# ENDPOINTS: ENTIDAD TRANSACCIONES
# =====================================================================

@app.get("/transacciones", response_model=list[TransaccionResponse])
def listar_transacciones():
    return lista_transacciones

@app.get("/transacciones/{transaccion_id}", response_model=TransaccionResponse)
def listar_transaccion_id(transaccion_id: int):
    for transaccion in lista_transacciones:
        if transaccion["id"] == transaccion_id:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.get("/transacciones/factura/{id_factura}", response_model=list[TransaccionResponse])
def listar_transacciones_factura(id_factura: int):
    filtradas = [t for t in lista_transacciones if t["id_factura"] == id_factura]
    return filtradas

@app.post("/transacciones", response_model=TransaccionResponse)
def crear_transaccion(transaccion: TransaccionCrear):
    nuevo_id = lista_transacciones[-1]["id"] + 1 if lista_transacciones else 1
    transaccion_dict = transaccion.model_dump()
    transaccion_dict["id"] = nuevo_id
    lista_transacciones.append(transaccion_dict)
    return transaccion_dict

@app.delete("/transacciones/{transaccion_id}", response_model=TransaccionResponse)
def eliminar_transaccion(transaccion_id: int):
    for indice, transaccion in enumerate(lista_transacciones):
        if transaccion["id"] == transaccion_id:
            return lista_transacciones.pop(indice)
    raise HTTPException(status_code=404, detail="Transacción no encontrada para eliminar")


# =====================================================================
# ENDPOINTS: ENTIDAD FACTURAS
# =====================================================================

@app.get("/facturas", response_model=list[FacturaResponse])
def listar_facturas():
    return lista_facturas

@app.get("/facturas/{factura_id}", response_model=FacturaResponse)
def obtener_factura_id(factura_id: int):
    for factura in lista_facturas:
        if factura["id"] == factura_id:
            return factura
    raise HTTPException(status_code=404, detail="Factura no encontrada")

@app.post("/facturas/{cliente_id}", response_model=FacturaResponse)
def crear_factura(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            cliente_encontrado = cliente
            break
            
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id} no existe."
        )
        
    nuevo_id = lista_facturas[-1]["id"] + 1 if lista_facturas else 1
    factura_dict = datos_factura.model_dump()
    factura_dict["id"] = nuevo_id
    factura_dict["id_cliente"] = cliente_id
    lista_facturas.append(factura_dict)
    return factura_dict