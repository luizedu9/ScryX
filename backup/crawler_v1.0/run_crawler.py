# -*- coding: utf-8 -*-

#	CIÊNCIA DA COMPUTAÇÃO
#
#	USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#	
#	Luiz Eduardo Pereira	
#
#	run_crawler.py:
#	Este modulo executa todos os outros modulos necessarios para o crawler

import os
import sys

os.system('scrapy runspider crawler/crawler/spiders/frantic_search.py -o text.csv -a request=' + sys.argv[1])