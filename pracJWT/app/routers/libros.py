from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from asyncio import sleep
from app.data.database import libros, prestamos
from app.models.models import Libro, Prestamo
from app.security.auth import verificar_peticion

routerU = APIRouter(
    prefix = "",
    tags= ['Crud HTTP']

)

@routerU.get("/")
def listar_libros():
    return libros

@routerU.post("/crear", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="Libro ya existe")
    libros.append(libro.dict())
    return {"mensaje": "Libro registrado"}

@routerU.get("/buscar/{nombre}")
def buscar_libro(nombre: str):
    resultado = [l for l in libros if nombre.lower() in l["nombre"].lower()]
    return resultado

@routerU.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):
    libro = next((l for l in libros if l["id"] == prestamo.libro_id), None)
    
    if not libro:
        raise HTTPException(status_code=400, detail="Libro no existe")

    if libro["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="Libro ya está prestado")

    libro["estado"] = "prestado"
    prestamos.append(prestamo.dict())
    return {"mensaje": "Préstamo registrado"}

@routerU.put("/devolver/{libro_id}")
def devolver_libro(libro_id: int):
    libro = next((l for l in libros if l["id"] == libro_id), None)

    if not libro:
        raise HTTPException(status_code=400, detail="Libro no existe")

    if libro["estado"] == "disponible":
        raise HTTPException(status_code=409, detail="No hay préstamo activo")

    libro["estado"] = "disponible"
    return {"mensaje": "Libro devuelto"}


@routerU.delete("/prestamos/{libro_id}")
def eliminar_prestamo(libro_id: int, userAuth:str = Depends(verificar_peticion)):
    prestamo = next((p for p in prestamos if p["libro_id"] == libro_id), None)

    if not prestamo:
        raise HTTPException(status_code=409, detail="Préstamo no existe")

    prestamos.remove(prestamo)
    return {f"mensaje": "Préstamo eliminado por {userAuth} con éxito"}