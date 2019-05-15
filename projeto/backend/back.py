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

from names_resolver import *


# CONECTA COM MONGODB
client = MongoClient('localhost',27017)
db = client["tcc"]

card_list = names_resolver(['1 Jace Beeren', '2 Fog Bank', '1 Descentelhar', '3 Abandon Hope'])

error_list = names_resolver(card_list)
if (len(error_list) == 0):
	db.crawler_queue.insert_one({'_id': '1', 'user': '1', 'cards': card_list})
	# TODO:
	# Liberar usuario
else:
	# TODO:
	# Retornar lista de nomes incorretos para usuario 
	print(error_list)