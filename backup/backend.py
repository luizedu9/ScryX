# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "super secret key"
app.config['TESTING'] = False
login_manager.session_protection = "strong"

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

# STATUS:
#   0 - SUCESSO
#   1 - OCORREU UM PROBLEMA INESPERADO
#   2 - USUARIO JA EXISTE
@app.route("/create_user", methods=['POST'])
def create_user():
    try:
        post_data = request.get_json()
        if user_exists(db, post_data.get("username")): # SE USUARIO JA EXISTE, NÃO CONTINUA
            return jsonify({'status': '2'})
        else:
            insert_user(db, User(
                post_data.get("username"),
                generate_password_hash(post_data.get("password")),
                post_data.get("name"),
                post_data.get("email"),
                post_data.get("birthdate"),
                post_data.get("gender")
                ))
            response_object = {'status': '0'}
    except:
        response_object = {'status': '1'}
    return jsonify(response_object)

# STATUS:
#   0 - SUCESSO
#   1 - OCORREU UM PROBLEMA INESPERADO
#   2 - USUARIO OU SENHA INCORRETOS
@app.route("/login", methods=['POST'])
def login():
    try:
        post_data = request.get_json()
        user = find_user(db, post_data.get("username")) # BUSCA USUARIO
        if (user != False):
            if (user.check_password(post_data.get("password"))): # CHECA SE SENHA ESTA CORRETA
                response_object = {'status': '0'}
                login_user(user, remember=True)
                print(current_user.username, file=sys.stderr)
            else:
                response_object = {'status': '2'}
        else:
            response_object = {'status': '2'} # USUARIO NÃO EXISTE
    except:
        response_object = {'status': '1'}
    return jsonify(response_object)

@app.route("/logout")
@login_required
def logout():
    response_object = {'status': '0'}
    logout_user()
    return jsonify(response_object)

# CRIAÇÃO DE REQUISIÇÃO DE COTAÇÃO DE PREÇO
# STATUS:
#   0 - SUCESSO
#   1 - OCORREU UM PROBLEMA INESPERADO
@app.route("/request_list", methods=['POST'])
def request_list():
    print(current_user.username, file=sys.stderr)
    post_data = request.get_json()
    try:
        error_list = register_request(db, post_data.get("card_list"), user_logged)
        if (error_list == []):
            response_object = {'status': '0'}
        else:
            response_object = {'error_list': error_list}
    except:
        response_object = {'status': '1'}
    return jsonify(response_object)

# INSERÇÃO DE CARTAS NO BANCO DE NOMES DE CARTAS
# STATUS:
#   0 - SUCESSO
#   1 - OCORREU UM PROBLEMA INESPERADO
@app.route("/insert_card_names", methods=['POST'])
@login_required
def insert_card_names():
    print('This is error output', file=sys.stderr)
    try:
        storage_cards(db, request.files['file'].read())
        response_object = {'status': '0'}   
    except:
        response_object = {'status': '1'}
    return jsonify(response_object)

@login_manager.user_loader
def user_loader(username):
    return find_user(db, username)
    
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

#print('This is error output', file=sys.stderr)
