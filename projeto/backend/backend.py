# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import uuid
from pymongo import MongoClient, errors
import logging as log
from unicodedata import normalize
from bson import ObjectId
import os
import sys

from db_request import *
from functions import *
from user import User

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

#######################################################################################################
#                                                                                                     #
#                                                 INIT                                                #
#                                                                                                     #
#######################################################################################################
# CONFIGURAÇÃO
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# ENABLE CORS
CORS(app, resources={r'/*': {'origins': '*'}})

user_logged = 1 # ********************************************************************

# CONECTA COM MONGODB
client = MongoClient('localhost', 27017)
try:
    # INICIA BD, SE NÃO EXISTIR, CRIA UM
    if ('scryx' not in client.list_database_names()):
        db = client["scryx"]
        insert_current_queue(db)
        insert_length_queue(db)
    else:
        db = client["scryx"]        
    client.server_info()
except:
    log.error('Can\'t connect to MongoDB')
    exit()

try: # CARREGA GERENCIADOR DE FILA
    current_queue = get_current_queue(db)
    length_queue = get_length_queue(db)
except:
    log.error('Can\'t read current_queue or length_queue')
    exit()

#######################################################################################################
#                                                                                                     #
#                                                 ROUTER                                              #
#                                                                                                     #
#######################################################################################################

# CRIAÇÃO DE USUARIO
# STATUS:
#   0 - SUCESSO
#   1 - USUARIO JA EXISTE
#   2 - HOUVE PROBLEMAS
@app.route("/create_user", methods=['POST'])
def create_user():
    if user_exists(db, request.values.get("username")): # SE USUARIO JA EXISTE, RETORNA 1
        response_object = {'status': '1'}
    else:
        try:
            insert_user(db, User(
                request.values.get("username"),
                request.values.get("password"),
                request.values.get("name"),
                request.values.get("email"),
                request.values.get("birthdate"),
                request.values.get("gender")
                ))
        except:
           response_object = {'status': '2'}
        return jsonify(response_object)

# CRIAÇÃO DE REQUISIÇÃO DE COTAÇÃO DE PREÇO
@app.route("/request_list", methods=['POST'])
def request_list():
    try:
        error_list = register_request(db, request.values.get("card_list"), user_logged)
        if (error_list == []):
            response_object = {'status': 'True'}
            print('DEU', file=sys.stderr)
        else:
            response_object = {'error_list': error_list}
            print('ERRADO DEU', file=sys.stderr)
    except:
        response_object = {'status': 'False'}
        print('NÃO DEU', file=sys.stderr)
    return jsonify(response_object)

# INSERÇÃO DE CARTAS NO BANCO DE NOMES DE CARTAS
@app.route("/insert_card_names", methods=['POST'])
def insert_card_names():
    storage_cards(db, request.files['file'].read())
    response_object = {'status': 'True'}   
    return jsonify(response_object)
    
#######################################################################################################
#                                                                                                     #
#                                                  EXEMPLO                                            #
#                                                                                                     #
#######################################################################################################

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

if __name__ == "__main__":
    app.run()
