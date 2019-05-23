# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   PARAMETROS: TXT COM A LISTA, ID DA EXECUÇÃO, ID USUARIO

from pymongo import MongoClient
from unicodedata import normalize
from contextlib import contextmanager
import os
import sys

from names_resolver import *

#######################################################################################################
#                                                                                                     #
#                                         INIT RESEARCH ASSISTANT                                     #
#                                                                                                     #
#######################################################################################################

# REFERENCIA: https://stackoverflow.com/questions/431684/how-do-i-change-directory-cd-in-python
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

# REFERENCIA: https://wiki.python.org.br/RemovedorDeAcentos
def accent_removal(cards):
    new_cards = []
    for card in cards:
        if (str(card).strip()): # SE VAZIO, IGNORA
            new_cards.append(normalize('NFKD', card).encode('ASCII', 'ignore').decode('ASCII').lower().strip())
    return new_cards

def request_to_dict(input_file):
    card_dict = {}
    card_file = open('requests/' + input_file, 'r', encoding="utf-8")
    cards = card_file.read().splitlines()
    cards = accent_removal(cards)
    for card in cards:
        if (str(card).strip()): # SE VAZIO, IGNORA
            card_dict[card.split(" ", 1)[1]] = card.split(" ", 1)[0] 
    card_file.close()
    return(card_dict)

def research_assistant(card_dict, _id, user):
    db.request_queue.insert_one({'_id': _id, 'user': user, 'cards': card_dict})
    with cd('../crawler'):
        os.system('python3 -B run_crawler.py ' +  _id + ' ' + 'saida.csv')
    with cd('../simulated_annealing'):
        os.system('python3 -B run_simulated_annealing.py')

#######################################################################################################
#                                                                                                     #
#                                                 BACK END                                            #
#                                                                                                     #
#######################################################################################################

# CONECTA COM MONGODB
client = MongoClient('localhost',27017)
db = client["tcc"]

card_dict = request_to_dict(sys.argv[1])
error_list = names_resolver(card_dict)
if (len(error_list) == 0):
    research_assistant(card_dict, sys.argv[2], sys.argv[3])
    # TODO:
    # Liberar usuario
else:
    # TODO:
    # Retornar lista de nomes incorretos para usuario 
    print(error_list) 