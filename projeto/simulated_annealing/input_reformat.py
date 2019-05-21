# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   input_reformat.py:
#   Este modulo tem como objetivo preparar os dados extraidos do crawler para iniciar a metaheuristica.
#
#       ESTRUTURA:
#                          LOJA
# CARTAS                  |   {0: 'A Taverna', | 1: 'Armada Nerd Hobby Store', | 2: 'Bahia Store'} |
# {0: ('time walk', 1),   |[(10, 0.3),(2, 1.0)]|           [(5, 10.0)]         |     [(2, 5.0)]    | 
# 1: ('descentelhar', 2)} |     [(2, 0.5)]|    |[(10, 0.5),(5, 0.9),(10, 15.0)]|[(5, 0.9),(2, 5.0)]|
#                                               LISTA[(QUANTIDADE, PREÇO), ...]
from pymongo import MongoClient
import csv

def list_reformat(_id):
    # CONECTA COM MONGODB
    client = MongoClient('localhost',27017)
    db = client["tcc"]
    # ADICIONA {ID CARTA: (NOME CARTA, QUANTIDADE CARTA)} NO DICIONARIO
    card_dict_temp = db.request_queue.find_one({'_id': _id}, {'cards': 1, '_id':0})
    cont = 0
    card_dict = {}
    for key, value in dict(sorted(card_dict_temp['cards'].items(), key=lambda kv: kv[0])).items():
        card_dict[cont] = ((key, int(value))) 
        cont += 1
    return(card_dict)

def crawler_reformat(csv_file, card_dict): 
    # ORDENA ARQUIVO CSV
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file, delimiter=",")
        sortedlist = sorted(reader, key=lambda row:(row['card'], row['store'], row['value'], row['quantity']), reverse=False)
    # CRIA UM DICIONARIO COM TODAS AS LOJAS QUE SERÃO UTILIZADAS
    store_dict_temp = {}
    cont_store = 0
    card_dict_temp = {}
    cont_card = 0
    for row in sortedlist:
        # ADICIONA 'ID LOJA: NOME LOJA' NO DICIONARIO
        if not(row['store'] in store_dict_temp):
            store_dict_temp[row['store']] = cont_store
            cont_store += 1
        if not(row['card'] in card_dict_temp):
            card_dict_temp[row['card']] = cont_card
            cont_card += 1
    # CRIA A MATRIZ DE CARTASX, LOJASY
    content_table = [[[] for x in range(len(store_dict_temp))] for y in range(len(card_dict_temp))] 
    for row in sortedlist:
        content_table[card_dict_temp[row['card']]][store_dict_temp[row['store']]].append((row['quantity'], row['value']))
    store_dict = dict(map(reversed, store_dict_temp.items()))
    return(card_dict, store_dict, content_table)

def run_input_reformat(card_id, crawler_file):
    return(crawler_reformat(crawler_file, list_reformat(card_id)))