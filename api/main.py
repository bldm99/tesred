#!/usr/bin/env python

import os
import json
import redis
from fastapi import FastAPI ,  HTTPException
import requests
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para permitir cualquier origen
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

@app.get("/")
async def index():
    return {"message": "Hello Worlds"}


@app.get("/alertas")
async def home():
    url = "https://girapi.bladimirchipana.repl.co/alumnos?_idUsuario=6531d08612ec096c58717b97&_idRiesgo=65754cdbd6a61db3295d8f3b"

    try:
        # Hacer la solicitud a la API externa
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción en caso de error HTTP

        # Obtener los datos JSON
        dataAPI = response.json()

        # Aquí puedes manipular los datos según tus necesidades
        return {"data": dataAPI}

    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud, como errores de red, timeout, etc.
        raise HTTPException(status_code=500, detail=f"Error al llamar a la API externa: {str(e)}")



