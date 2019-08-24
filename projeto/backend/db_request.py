# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    

from pymongo import MongoClient, errors

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
            '_id': str(user.username),
            'password': str(user.password),
            'name': str(user.name),
            'email': str(user.email),
            'birthdate': str(user.birthdate),
            'gender': str(user.gender),
            'entrydate': str(user.entrydate),
            'budget': {}})
        return(0)
    except errors.DuplicateKeyError:
        return(1)

#######################################################################################################
#                                                                                                     #
#                                            BD_REQUEST_QUEUE                                         #
#                                                                                                     #
#######################################################################################################

def insert_request(db, id_request, id_user, card_dict):
    db.request.insert_one({'_id': id_request, 'user': id_user, 'cards': card_dict})

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
