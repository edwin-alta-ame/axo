from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
import jwt
import os
import psycopg2
import hashlib
import time
import functools,base64
from dotenv import load_dotenv
load_dotenv()

#Variables para conexión a base de datos
pg_conn_data = {"host":os.getenv('HOST'),"user":os.getenv('USER'),"password":os.getenv('PASS'),"db":os.getenv('DB'),"port":os.getenv('PORT')}
#Variables
parser = reqparse.RequestParser()
token_key = "PXrvFaomZlEVWm8r1ClzfRmacBYYAdzoAqkQ6YDgJRBqDJhFWTFCuK2XWah6EDA"
app_testing = False

import junglebranchs.token
import junglebranchs.dbpg


