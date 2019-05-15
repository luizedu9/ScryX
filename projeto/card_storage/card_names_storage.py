# -*- coding: utf-8 -*-

#	CIÊNCIA DA COMPUTAÇÃO
#
#	USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#	
#	Luiz Eduardo Pereira	
#
#	card_names_storage.py:
#	Este modulo realiza a filtragem de dados extraindo os nomes em ingles e portugues das cartas de magic
#	Um arquivo AllCards.json é requerido como entrada para leitura dos dados
#	O arquivo AllCards.json é disponibilizado pelo projeto 'mtgjson.com'
#
#	python3 card_names_storage.py

import json
from pymongo import MongoClient
from unicodedata import normalize

# REFERENCIA: https://wiki.python.org.br/RemovedorDeAcentos
def accent_removal(string):
	return normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')

# CONECTA COM MONGODB
client = MongoClient('localhost',27017)
db = client["tcc"]
card = db.card

# ABRE ARQUIVO JSON
file = open('AllCards.json', 'r', encoding="utf-8")
content = file.read()
dictionary = json.loads(content)
file.close()

# PEGA CADA NOME DE CARTA EM INGLES E PORTUGUES E ARMAZENA NO BANCO
for key in dictionary:
	card_english = accent_removal(key).lower()
	card_portuguese = ''
	for element in dictionary[key]['foreignData']:
		if (element['language'] == 'Portuguese (Brazil)'):
			card_portuguese = accent_removal(element['name'].lower())
	try:
		card.insert_one({'_id': card_english, 'portuguese': card_portuguese})
	except:
		pass