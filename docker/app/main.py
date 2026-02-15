from fastapi import FastAPI, HTTPException
from typing import Optional
import asyncio

app = FastAPI(
    title="fast api",
    description="my first api from fastapi",
    version="1.0.0"
)

usuarios = [
    {"id": 1, "nombre": "benjamin", "email": "ben@gmail.com"},
    {"id": 2, "nombre": "benjamin", "email": "ben@gmail.com"},
    {"id": 3, "nombre": "benjamin", "email": "ben@gmail.com"},
]

@app.get("/", tags=["Home"])
def home():
    return {"mensaje": "Hola ben"}

@app.get("/v1/bienvenidos", tags=["Home"])
def bienvenidos():
    return {"mensaje": "Hola y bienvenido"}

@app.get("/v1/promedio", tags=["Promedio"])
async def promedio():
    await asyncio.sleep(3)
    return {"calificación": 7.5, "estatus": 200}

@app.get("/v1/usuario/{id}", tags=["Usuario"])
def consulta(id: int):
    return {"mensaje": "user found", "status": 200, "id": id}

@app.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2)

    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado": id, "Datos": usuario}
        return {"Mensaje": "usuario no encontrado"}
    else:
        return {"Aviso": "No se proporcionó Id"}

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consulta1():
    return {"status": 200, "total": len(usuarios), "data": usuarios}

@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crea_usuario(usuario: dict):
    if "id" not in usuario:
        raise HTTPException(status_code=400, detail="Falta el campo 'id'")

    for usr in usuarios:
        if usr["id"] == usuario["id"]:
            raise HTTPException(status_code=400, detail="el id ya existe")

    usuarios.append(usuario)
    return {"mensaje": "Usuario creado correctamente", "status": 200}

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: dict):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            actualizado = {**usr, **usuario, "id": id}
            usuarios[i] = actualizado
            return {"mensaje": "Usuario actualizado", "status": 200, "usuario": actualizado}

    raise HTTPException(status_code=404, detail="usuario no encontrado")

@app.delete("/v1/usuario/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id: int):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(i)
            return {"mensaje": "Usuario Eliminado", "status": 200, "usuario_eliminado": eliminado}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")
