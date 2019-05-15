# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   names_resolver.py:
#   Este modulo verifica se as cartas passadas pelo usuario existem
#   Se o retorno deste modulo for uma lista não vazia, significa que o usuario digitou cartas inexistente, impedindo o prosseguimento do programa

from pymongo import MongoClient
from unicodedata import normalize

# REFERENCIA: https://wiki.python.org.br/RemovedorDeAcentos
def accent_removal(cards):
    new_cards = []
    for card in cards:
        if (str(card).strip()): # SE VAZIO, IGNORA
            new_cards.append(normalize('NFKD', card).encode('ASCII', 'ignore').decode('ASCII').lower().strip())
    return new_cards

def names_resolver(card_list):
    
    # CONECTA COM MONGODB
    client = MongoClient('localhost',27017)
    db = client["tcc"]
    card = db.card

    card_list = accent_removal(card_list)
    error_list = []
    for iterator in card_list:
        card_splited = iterator.split(" ", 1)
        # VERIFICA SE OS PARAMETROS FORAM PASSADOS CORRETAMENTE. (QUANTIDADE, NOME, PRIORIDADE 'opcional')
        if ((len(card_splited) < 2) and (len(card_splited) > 3)):
            error_list.append(iterator)
        else:
            card_name = card_splited[1]
            # VERIFICA SE A CARTA PASSADA NÃO SE ENCONTRA EM NO BANCO DE DADOS EM INGLES OU PORTUGUES
            if (not(card.find_one({'_id': card_name}) or card.find_one({'portuguese': card_name}))):
                error_list.append(iterator)
    return(error_list)