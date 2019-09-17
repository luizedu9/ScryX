# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    

from pymongo import MongoClient, errors
import json
import sys
from bson.json_util import dumps

from user import User

#######################################################################################################
#                                                                                                     #
#                                                 BD_CARD                                             #
#                                                                                                     #
#######################################################################################################

def find_name_english(db, name):
    try:
        if (db.card.find_one({'_id': name}) != None):
            return(True)
        else:
            return(False)
    except:
        raise

def find_name_portuguese(db, name):
    try:
        if (db.card.find_one({'portuguese': name}) != None):
            return(True)
        else:
            return(False)
    except:
        raise

def insert_card(db, card_english, card_portuguese):
    try:
        db.card.insert_one({'_id': card_english, 'portuguese': card_portuguese})
    except errors.DuplicateKeyError:
        pass
    except:
        raise

#######################################################################################################
#                                                                                                     #
#                                                 BD_USER                                             #
#                                                                                                     #
#######################################################################################################

def insert_user(db, user):
    try:
        db.user.insert_one({
            '_id': user.username,
            'password': user.password,
            'name': user.name,
            'email': user.email,
            'birthdate': str(user.birthdate),
            'entrydate': str(user.entrydate),
            'admin': user.admin})
        return(True)
    except errors.DuplicateKeyError:
        return(False)

def user_exists(db, username):
    if (db.user.find_one({'_id': username}) != None):
        return(True)
    else:
        return(False)


def email_exists(db, email):
    if (db.user.find_one({'email': email}) != None):
        return(True)
    else:
        return(False)

def find_user(db, username):
    try:
        result = db.user.find_one({'_id': username})
        user = User(result['_id'], result['password'], result['name'],
                    result['email'], result['birthdate'], 
                    result['entrydate'], result['admin'])
    except:
        user = None
    return(user)

def update_email(db, username, email):
    try:
        return(db.user.update_one({'_id': username}, {'$set': {'email': email}}))
    except:
        return(None)

def update_password(db, username, password):
    try:
        return(db.user.update_one({'_id': username}, {'$set': {'password': password}}))
    except:
        return(None)

def delete_user(db, username):
    try:
        db.user.delete_one({'_id': username})
        return(True)
    except:
        return(False)

#######################################################################################################
#                                                                                                     #
#                                            BD_REQUEST_QUEUE                                         #
#                                                                                                     #
#######################################################################################################

def insert_request(db, id_request, id_user, card_dict):
    try:
        db.request.insert_one({'_id': id_request, 'user': id_user, 'cards': card_dict, 'crawler': []})
    except:
        return(None)

#######################################################################################################
#                                                                                                     #
#                                            BD_REQUEST_QUEUE                                         #
#                                                                                                     #
#######################################################################################################

def find_result(db, username):
    try:
        return(dumps(db.result.find({'user': username})))
    except:
        return(None)

#######################################################################################################
#                                                                                                     #
#                                            BD_QUEUE_MANAGER                                         #
#                                                                                                     #
#######################################################################################################

# RETORNA A POSIÇÃO ATUAL QUE O PROGRAMA ESTÁ NA FILA
def get_current_queue(db):
    return(db.queue.find_one({'_id': 'current_queue'}, { '_id': 0, 'value': 1})['value'])

def insert_current_queue(db):
    db.queue.insert_one({'_id': 'current_queue', 'value': '0'})

# INCREMENTA CURRENT_QUEUE
def increment_current_queue(db):
    db.queue.update_one({'_id': 'current_queue'}, {'$set': {'value': str(int(get_current_queue(db))+1)}})

# RETORNA O TAMANHO DA FILA
def get_length_queue(db):
    return(db.queue.find_one({'_id': 'length_queue'}, {'_id': 0, 'value': 1})['value'])

def insert_length_queue(db):
    db.queue.insert_one({'_id': 'length_queue', 'value': '0'})

# INCREMENTA LENGTH_QUEUE
def increment_length_queue(db):
    db.queue.update_one({'_id': 'length_queue'}, {'$set': {'value': str(int(get_length_queue(db))+1)}})
