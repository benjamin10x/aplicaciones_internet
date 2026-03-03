from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

app = FastAPI(title="Biblioteca Digital")

libros = []
prestamos = []

# MODELOS

class Usuario(BaseModel):
    nombre: str
    correo: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v):
        if not re.match(r"^[a-zA-Z\s]+$", v):
            raise ValueError("Nombre inválido")
        return v

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Correo inválido")
        return v

class Libro(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int
    paginas: int = Field(..., gt=1)
    estado: str = "disponible"

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v):
        if v not in ["disponible", "prestado"]:
            raise ValueError("Estado inválido")
        return v

    @field_validator("año")
    @classmethod
    def validar_año(cls, v):
        año_actual = datetime.now().year
        if v <= 1450 or v > año_actual:
            raise ValueError("Año inválido")
        return v

class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario

# ENDPOINTS

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="Libro ya existe")
    libros.append(libro.dict())
    return {"mensaje": "Libro registrado"}

@app.get("/libros")
def listar_libros():
    return libros

@app.get("/libros/buscar/{nombre}")
def buscar_libro(nombre: str):
    resultado = [l for l in libros if nombre.lower() in l["nombre"].lower()]
    return resultado

@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):
    libro = next((l for l in libros if l["id"] == prestamo.libro_id), None)
    
    if not libro:
        raise HTTPException(status_code=400, detail="Libro no existe")

    if libro["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="Libro ya está prestado")

    libro["estado"] = "prestado"
    prestamos.append(prestamo.dict())
    return {"mensaje": "Préstamo registrado"}

@app.put("/devolver/{libro_id}")
def devolver_libro(libro_id: int):
    libro = next((l for l in libros if l["id"] == libro_id), None)

    if not libro:
        raise HTTPException(status_code=400, detail="Libro no existe")

    if libro["estado"] == "disponible":
        raise HTTPException(status_code=409, detail="No hay préstamo activo")

    libro["estado"] = "disponible"
    return {"mensaje": "Libro devuelto"}

@app.delete("/prestamos/{libro_id}")
def eliminar_prestamo(libro_id: int):
    prestamo = next((p for p in prestamos if p["libro_id"] == libro_id), None)

    if not prestamo:
        raise HTTPException(status_code=409, detail="Préstamo no existe")

    prestamos.remove(prestamo)
    return {"mensaje": "Préstamo eliminado"}