from fastapi import FastAPI
from app.routers import libros


app=FastAPI()

app.include_router(libros.routerU)

