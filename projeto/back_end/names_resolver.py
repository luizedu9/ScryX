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

def names_resolver(card_dict):
    
    # CONECTA COM MONGODB
    client = MongoClient('localhost',27017)
    db = client["tcc"]
    card = db.card

    error_list = []
    for key, value in card_dict.items():
        # VERIFICA SE OS PARAMETROS FORAM PASSADOS CORRETAMENTE. (QUANTIDADE, NOME)
        if (not(value.isdigit())):
            error_list.append(key)
        else:
            # VERIFICA SE A CARTA PASSADA NÃO SE ENCONTRA EM NO BANCO DE DADOS EM INGLES OU PORTUGUES
            if (not(card.find_one({'_id': key}) or card.find_one({'portuguese': key}))):
                error_list.append(key)
    return(error_list)