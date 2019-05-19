# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   *********************************************************

from pymongo import MongoClient
from unicodedata import normalize
import os

from names_resolver import *

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

# CONECTA COM MONGODB
client = MongoClient('localhost',27017)
db = client["tcc"]

card_dict = request_to_dict('lista_pequena.txt')
error_list = names_resolver(card_dict)
if (len(error_list) == 0):
    db.request_queue.insert_one({'_id': '1', 'user': '1', 'cards': card_dict})
    os.system('scrapy crawl crawler -a id=' +  '1' + ' -o ' + 'saida.csv' + ' -t csv')
    # TODO:
    # Liberar usuario
else:
    # TODO:
    # Retornar lista de nomes incorretos para usuario 
    print(error_list) 