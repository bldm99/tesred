#!/usr/bin/env python

import os
import json
import redis
from fastapi import FastAPI ,  HTTPException
import requests
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import math

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
        response = requests.get(url)
        response.raise_for_status()  
        dataAPI = response.json()

        df = pd.DataFrame(dataAPI)
        newdf = df[['_id', 'sem1', 'sem2']]

        diccionarioapi = {}
        newdf.set_index('_id').apply(lambda row: diccionarioapi.update({row.name: row.dropna().to_dict()}), axis=1)
        

         # Manhattan distance
        def manhattanL(user1, user2):
            dist = 0.0
            count = 0
            for i in user2:
                if not (user1.get(i) is None):
                    x = user1[i]
                    y = user2[i]
                    dist += abs(x - y)
                    count += 1

            if count == 0:
                return 9999.99
            return dist
        
                # Init K-vector with correct value based on distance type
        def initVectDist(funName, N):
            if funName == 'euclidiana' or funName == 'manhattan' or funName == 'euclidianaL' or funName == 'manhattanL':
                ls = [99999] * N
            else:
                ls = [-1] * N

            lu = [None] * N
            return ls, lu


        # Keep the closest values, avoiding sort
        def keepClosest(funname, lstdist, lstuser, newdist, newuser, N):
            if funname == 'euclidiana' or funname == 'manhattan' or funname == 'euclidianaL' or funname == 'manhattanL':
                count = -1
                for i in lstdist:
                    count += 1
                    if newdist > i:
                        continue
                    lstdist.insert(count, newdist)
                    lstuser.insert(count, newuser)
                    break
            else:
                count = -1
                for i in lstdist:
                    count += 1
                    if newdist < i:
                        continue
                    lstdist.insert(count, newdist)
                    lstuser.insert(count, newuser)
                    break

            if len(lstdist) > N:
                lstdist.pop()
                lstuser.pop()
            return lstdist, lstuser
        
                # K-Nearest neighbour
        def knn_L(N, distancia, usuario, data):  # N numero de vecinos
            funName = distancia.__name__
            print('k-nn', funName)

            listDist, listName = initVectDist(funName, N)
            nsize = len(data)
            otherusers = range(0, nsize)
            vectoruser = data.get(usuario)
            claves_principales = list(data.keys())

            for i in claves_principales: #recorre de 0 a cantidad de datos del diicionario digamos 10
                tmpuser = i
                if tmpuser != usuario:
                    tmpvector = data.get(tmpuser)
                    if not (tmpvector is None):
                        tmpdist = distancia(vectoruser, tmpvector)
                        if tmpdist is not math.nan:
                            listDist, listName = keepClosest(funName, listDist, listName, tmpdist, tmpuser, N)

            return listDist, listName
        
        def topSuggestions(fullObj, k, items):
            rp = [-1]*items

            for i in fullObj:
                rating = fullObj.get(i)

                for j in range(0, items):
                    if rp[j] == -1 :
                        tmp = [i, rating[0], rating[1]]
                        rp.insert(j, tmp)
                        rp.pop()
                        break
                    else:
                        tval = rp[j]
                        if tval[1] < rating[0]:
                            tmp = [i, rating[0], rating[1]]
                            rp.insert(j, tmp)
                            rp.pop()
                            break

            return rp
        
        def recommendationL(usuario, distancia, N, items, minr, data):
            ldistK, luserK = knn_L(N, distancia, usuario, data)

            user = data.get(usuario)
            recom = [None] * N
            for i in range(0, N):
                recom[i] = data.get(luserK[i])
            # print('user preference:', user)

            lstRecomm = [-1] * items
            lstUser = [None] * items
            lstObj = [None] * items
            k = 0

            fullObjs = {}
            count = 0
            for i in recom:
                for j in i:
                    tmp = fullObjs.get(j)
                    if tmp is None:
                        fullObjs[j] = [i.get(j), luserK[count]]
                    else:
                        nval = i.get(j)
                        if nval > tmp[0]:
                            fullObjs[j] = [nval, luserK[count]]
                count += 1

            finallst = topSuggestions(fullObjs, count, items)
            return finallst
        
        cant_usuaruios = len(diccionarioapi) - 1
        rfuncs = manhattanL
        userselect = '6575cd66ab54236e314707f9'
        mnha = knn_L(cant_usuaruios, rfuncs, userselect, diccionarioapi)

        correosx = [identifier for value, identifier in zip(*mnha) if value == 0.0]
        dic_correo = {}  
        dic_correo["correosx"] = correosx
    
        return dic_correo

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a la API externa: {str(e)}")



