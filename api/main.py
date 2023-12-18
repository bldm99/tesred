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
from datatable import dt, f, by, g, join, sort, update, ifelse
import ast

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

idinit = "y433r"
clave_redis_id = "ids_"+ idinit
redis_conn.set(clave_redis_id, idinit)

csv_patht = '/shared_data/finaldata.csv'

@app.get("/")
async def index():
    return {"message": "Hello Worlds"}


@app.get("/alertas")
async def home():
    url = "https://girapi.bladimirchipana.repl.co/alumnos?_idUsuario=6531d08612ec096c58717b97&_idRiesgo=657f1edfb8453f2c73ddf88c"
    #urltecsup = "http://localhost:3000/estudiantes"

    try:
        #Data alumnos nuevos
        response = requests.get(url)
        response.raise_for_status()  
        dataAPI = response.json()

        #Data historial alumnos que ya estudiaron en tecsup
        '''responsetecsup = requests.get(urltecsup)
        responsetecsup.raise_for_status()  
        dataTecsup = responsetecsup.json()'''

        
        

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
        
        #Dataframe de historial de asistencias de alumnos de tecsup
        #dftecsup = pd.DataFrame(dataTecsup)
        #csv_path = 'finaldata.csv'
        dftecsup = dt.fread(csv_patht).to_pandas()
        dftecsup['sem1'] = dftecsup['sem1'].astype(int)
        dftecsup['sem2'] = dftecsup['sem2'].astype(int)
        dftecsup['sem3'] = dftecsup['sem3'].astype(int)
        dftecsup['sem4'] = dftecsup['sem4'].astype(int)
        dftecsup['sem5'] = dftecsup['sem5'].astype(int)
        dftecsup['sem6'] = dftecsup['sem6'].astype(int)
        dftecsup['sem7'] = dftecsup['sem7'].astype(int)
        dftecsup['sem8'] = dftecsup['sem8'].astype(int)
        dftecsup['sem9'] = dftecsup['sem9'].astype(int)
        dftecsup['sem10'] = dftecsup['sem10'].astype(int)
        dftecsup['sem11'] = dftecsup['sem11'].astype(int)
        dftecsup['sem12'] = dftecsup['sem12'].astype(int)
        dftecsup['sem13'] = dftecsup['sem13'].astype(int)
        dftecsup['sem14'] = dftecsup['sem14'].astype(int)
        dftecsup['sem15'] = dftecsup['sem15'].astype(int)
        dftecsup['sem16'] = dftecsup['sem16'].astype(int)
        dftecsup= dftecsup.head(5000)
        
        #Dataframe de alumnos nuevos
        df = pd.DataFrame(dataAPI)

        #Si la cantidad de columas es 7 tomaremso las distancias de 0.0
        num_filas, num_columnas = df.shape
        dic_correo = {} 

        #Traemos solo las columnas que nso interesan
        newdf = df.iloc[:, 4:] 

        #eliminamos todas las filas ids que tiene ids ya usados , para que no repitan el proceso
        keys = redis_conn.keys("ids_*")
        values = [redis_conn.get(key).decode() for key in keys]

        # Filtrar el DataFrame para excluir las filas con _id en la lista 'values'
        newdf = newdf[~newdf['_id'].isin(values)]



        num_f, num_c = newdf.shape
        newdftecsup = dftecsup.iloc[:, 4:] 
        diccionarioapi = {}
        
        
        if num_columnas >= 7:

            #Obtenemos todas las columas de sem que estan presentes
            nombre_columnas = newdf.columns[1:]
            # Calculamos la suma de las columnas para cada Id y convertir a un diccionario
            sumas = newdf.set_index('_id')[nombre_columnas].sum(axis=1).to_dict()

            #Almacenamos en una lista todas las claves cuya suma dio valor de 2
            valor_dos = [key for key, value in sumas.items() if value == 2] 
            


            li = []

            for  r in valor_dos:
                dataframe_actual = newdf[newdf['_id'] == r] #4columnas
                num_fil, num_colaistencia = dataframe_actual.shape

                #obtenemos los nombre de las sem donde el valor sea 1
                semanas = dataframe_actual.iloc[0, 1:][dataframe_actual.iloc[0, 1:] == 1].index.tolist()

                #Buscamos en el dataframe tecsup osea newdftecsup  todos los alumnos que tienen el valor de 1 en las
                #diferentes semanas
                resultadosz = newdftecsup.query(f'{semanas[0]} == 1 and {semanas[1]} == 1')
                #semanas.append(r)
                
                
                igualar_columnas = resultadosz.iloc[:, :num_colaistencia]
                n, c = igualar_columnas.shape

                
                #Procedemos a concatenera dataframe_actual con resultadosz para hallar los vecinos cercanos
                union = pd.concat([dataframe_actual , igualar_columnas])
                diz = {}
                union.set_index('_id').apply(lambda row: diz.update({row.name: row.dropna().to_dict()}), axis=1)

                

                cant_usuaruios = len(diz) - 1
                rfuncs = manhattanL
                userselect = r
                mnha = knn_L(cant_usuaruios, rfuncs, userselect, diz)
                hola = mnha[1]

                #correosx vendria aser todos los id dealumnos tque tiene una distancia de 0.0
                correosx = [identifier for value, identifier in zip(*mnha) if value == 0.0]

                #Buscamos todos esos id en los datos de historial
                dat = newdftecsup.query('_id in @correosx')
                n, c = dat.shape
                #Solo necesitamos las columnas de las semanas posteriores y no las que ya pasaron
                recort = dat.iloc[:, num_colaistencia:]
                conteo_1_por_columna = recort.sum()
                conteo_dict = conteo_1_por_columna.to_dict()

                #Maximos valores
                max_value = max(conteo_dict.values())
                columnas_con_max_valor = [col for col, valor in conteo_dict.items() if valor == max_value]
                resultado_final = {col: max_value for col in columnas_con_max_valor}

                #obtenemos datos del alumno
                datalumno = df.loc[df['_id'] == r]
    
                # Obtener una lista con los valores de 'nombre' y 'correo' para cada fila filtrada
                listalumno = datalumno[['nombre', 'correo','_id']].values.flatten().tolist()

                nuevo_diccionario = {'alumno': listalumno[0],'correo': listalumno[1], **resultado_final}
                li.append(nuevo_diccionario)

                #Alamcenando datos para analisis de l alumno
                clave_redis = f"mi_clave_{listalumno[2]}"
                redis_conn.set(clave_redis, str(nuevo_diccionario))

                #Almacenando solo id 
                clave_id = f"ids_{listalumno[2]}"
                redis_conn.set(clave_id, listalumno[2])

                
                






        '''if num_columnas > 7:
            #newdf = df[['_id', 'sem1', 'sem2']]
            #newdf = df.iloc[:, 4:]
            #diccionarioapi = {}

            newdf.set_index('_id').apply(lambda row: diccionarioapi.update({row.name: row.dropna().to_dict()}), axis=1)
            
            cant_usuaruios = len(diccionarioapi) - 1
            rfuncs = manhattanL
            userselect = '6575cd66ab54236e314707f9'
            mnha = knn_L(cant_usuaruios, rfuncs, userselect, diccionarioapi)

            correosx = [identifier for value, identifier in zip(*mnha) if value == 1.0]
            #buscar correos de los ids obtenidos 
            rae = df.query('_id in @correosx')
            framecorreo = rae[['nombre', 'correo']]
            #dic_correo = {}  
            dic_correo = framecorreo.to_dict(orient='records')
            #dic_correo["correosx"] = correosx '''

    
        #return dic_correo
        #return semanas
        #return li
        return resultado_final

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a la API externa: {str(e)}")

@app.get("/resultados")
async def resul():
    try:
        
        # Obtener todas las claves que coinciden con el patrón "mi_clave_*"
        keys = redis_conn.keys("mi_clave_*")
        #keys = redis_conn.keys("ids_*")

        # Obtener los valores asociados con las claves
        values = [ast.literal_eval(redis_conn.get(key).decode()) for key in keys]
        #values = [redis_conn.get(key).decode() for key in keys]


        return JSONResponse(content=values)
    
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a la API Tecsup: {str(e)}")


@app.get("/tecsup")
async def tecsup():
    urltecsup = "http://localhost:3000/estudiantes"

    try:
        '''response = requests.get(urltecsup)
        response.raise_for_status()  
        dataAPI = response.json()'''

        #Pruebas de codigo---------------------
        csv_path = 'datosx.csv'
        #midf = pd.read_csv(csv_path , sep=";")
        midf = dt.fread(csv_path).to_pandas()
        #midf.replace({True: 1, False: 0}, inplace=True)
        midf['sem1'] = midf['sem1'].astype(int)
        midf['sem2'] = midf['sem2'].astype(int)
        midf['sem3'] = midf['sem3'].astype(int)
        midf['sem4'] = midf['sem4'].astype(int)
        midf['sem5'] = midf['sem5'].astype(int)
        midf['sem6'] = midf['sem6'].astype(int)
        midf['sem7'] = midf['sem7'].astype(int)
        midf['sem8'] = midf['sem8'].astype(int)
        midf['sem9'] = midf['sem9'].astype(int)
        midf['sem10'] = midf['sem10'].astype(int)
        midf['sem11'] = midf['sem11'].astype(int)
        midf['sem12'] = midf['sem12'].astype(int)
        midf['sem13'] = midf['sem13'].astype(int)
        midf['sem14'] = midf['sem14'].astype(int)
        midf['sem15'] = midf['sem15'].astype(int)
        midf['sem16'] = midf['sem16'].astype(int)
        midf = midf.head(5)

        diz = {}
        midf.set_index('_id').apply(lambda row: diz.update({row.name: row.dropna().to_dict()}), axis=1)



        #return dataAPI
        return diz
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a la API Tecsup: {str(e)}")