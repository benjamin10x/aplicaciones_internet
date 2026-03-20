from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

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