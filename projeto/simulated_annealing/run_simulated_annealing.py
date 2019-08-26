# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   run_simulated_annealing.py:
#   Este modulo tem como objetivo iniciar a metaheuristica.
#
#	python3 run_simulated_annealing.py id_request id_user/saida.csv

import os
import sys

repeat_mode = True # CHECA SE O MODO CSV ESTÁ HABILITADO, SE TIVER, UTILIZA 3 PARAMETROS
try:
	_ = sys.argv[3]
except:
	repeat_mode = False

if repeat_mode:
	repeat = 1 # QUANTAS VEZES IRÁ REPETIR O SIMULATED ANNEALING
	for i in range(repeat):
		print(str("%.2f"%((i * 100) / repeat)) + '%')
		os.system('python3 -B simulated_annealing.py ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3])
	print("100%")
else:
	os.system('python3 -B simulated_annealing.py ' + sys.argv[1] + ' ' + sys.argv[2])
