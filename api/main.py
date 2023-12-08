#!/usr/bin/env python

import os
import json
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS , cross_origin
import pandas as pd
from linkextractor import columnas
import numpy as np
from scipy.spatial.distance import cityblock
import math
from datatable import dt, f, by, g, join, sort, update, ifelse






app = Flask(__name__)
CORS(app)


redis_conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))




@app.route("/")
def index():
    return "Usage: http://<hostname>[:<prt>]/api/<url>"

#----------------------------------------------------------------
total = {}
valoresfinal = {}
peliculasp = {}
usuariosp = {}
df = pd.DataFrame()
midf = pd.DataFrame()
movie_ids_user1 = []
csv_path = '/shared_data/movie.csv'

@app.route('/api/csv', methods=['POST'])
def recibir_csv():
    global df
    global midf
    global usuariosp
    global movie_ids_user1
    if request.method == 'POST':
        data = request.get_json()  
        theuser = data.get('user')  
        theuserx = int(theuser)

       
        
        return jsonify({"mensaje": theuser})
    else:
        return jsonify({"mensaje": "Esta ruta solo acepta solicitudes POST"})





app.run(host="0.0.0.0")
