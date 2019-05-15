# -*- coding: utf-8 -*-

#	CIÊNCIA DA COMPUTAÇÃO
#
#	USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#	
#	Luiz Eduardo Pereira	
#
#	run_crawler.py:
#	Este modulo executa todos os outros modulos necessarios para o crawler
#
#	python3 run_crawler.py lista_pequena.txt saida
#
#	V 2.0

import os
import sys

os.system('scrapy crawl crawler -a input_file=' +  sys.argv[1] + ' -o ' + sys.argv[2] + ' -t csv')
