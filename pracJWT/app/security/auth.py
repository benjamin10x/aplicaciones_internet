from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException, Depends
import secrets


seguridad = HTTPBasic()

def verificar_peticion(credentiales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth = secrets.compare_digest(credentiales.username, "admin")
    passAuth = secrets.compare_digest(credentiales.password, "admin123")

    if not (userAuth and passAuth):
        raise HTTPException(status_code=401, detail="Credenciales no autorizadas")
    
    else:
        return credentiales.username