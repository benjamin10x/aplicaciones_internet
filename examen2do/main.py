from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


app = FastAPI()
# sencilla, suite, doble
reservas = []

tipo_habitacion = ["sencilla", "suite", "doble"]

class Reserva(BaseModel):
    id: int
    nombre_huesped: str = Field(..., min_length=5)
    fecha_entrada: datetime = Field(..., description="Fecha de entrada ")
    fecha_salida: datetime = Field(..., description="Fecha de salida ")
    tipo_habitacion: str
    confirmado: bool = False
    estancia: int = Field(..., description="Duración de la estancia en días", ge=0, le=7)

    @field_validator('tipo_habitacion')
    @classmethod
    def validar_tipo_habitacion(cls, v):
        if v not in tipo_habitacion:
            raise ValueError(f'Tipo de habitación debe ser uno de: {tipo_habitacion}')
        return v


seguridad = HTTPBasic()

def verificar_usuario(credentials: HTTPBasicCredentials = Depends(seguridad)):
    usuario_valido = secrets.compare_digest(credentials.username, "hotel")
    contrasena_valida = secrets.compare_digest(credentials.password, "r2026")
    if not (usuario_valido and contrasena_valida):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
# datos
# huesped minimo 5 caracteres
# fecha entrada no menor a fecha actual
# fecha salida no menor a fecha entrada
# la estancia no puede ser mayor a 7 dias






# Crear reserva
@app.post("/reservas", status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: Reserva):
    if reserva.fecha_entrada.date().day < datetime.now().date().day:
        raise HTTPException(status_code=400, detail="La fecha de entrada no puede ser menor a la fecha actual.")
    if reserva.fecha_salida < reserva.fecha_entrada:
        raise HTTPException(status_code=400, detail="La fecha de salida no puede ser menor a la fecha de entrada.")
    estancia = (reserva.fecha_salida - reserva.fecha_entrada).days
    if estancia > 7:
        raise HTTPException(status_code=400, detail="La estancia no puede ser mayor a 7 días.")
    reserva.estancia = estancia
    reservas.append(reserva)
    return reserva




# listar reservas 
@app.get("/reservas")
def listar_reservas():
    return reservas



# consultar por ID
@app.get("/reservas/{reserva_id}")
def consultar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva.id == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail="Reserva no encontrada")


# endpoint protegidos por autenticacion basica

# confirmar reserva
@app.post("/reservas/{reserva_id}/confirmar")
def confirmar_reserva(reserva_id: int, credentials: HTTPBasicCredentials = Depends(verificar_usuario)):
    for reserva in reservas:
        if reserva.id == reserva_id:
            reserva.confirmado = True
            return {"message": "Reserva confirmada"}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")    



# eliminar reserva
@app.delete("/reservas/{reserva_id}")
def eliminar_reserva(reserva_id: int, credentials: HTTPBasicCredentials = Depends(verificar_usuario)):
    for i, reserva in enumerate(reservas):
        if reserva.id == reserva_id:
            del reservas[i]
            return {"message": "Reserva eliminada"}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")







