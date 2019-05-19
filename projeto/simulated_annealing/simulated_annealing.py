# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   simulated_annealing.py:
#   Este modulo é a metaheuristica do projeto. Utiliza como entrada a lista de lojas e cartas que foi o resultado do crawler.
#   A metaheuristica escolhida foi o Simulated Annealing, processo que utiliza um espaço de busca de vizinhança para tentar 
#   encontrar o melhor resultado. Utiliza um sistema de temperatura, que vai diminuindo de acordo com as iterações do programa.
#   Quando está no estado de temperatura alta, é aplicado um criterio de aceitação, tendo maior probabilidade de se aceitar uma
#   mudança de vizinho sem que é considerado mais ruim, quando a temperatura está mais abaixo, o criterio fica mais seletivo
#   tendo probabilidade maior de aceitar somente resultados bons. Isso é feito para se evitar optimos locais.
#
#   Versão 1.0 - Implementação do primeiro pseudocodigo do artigo "Pareto Simulated Annealing"

from input_reformat import *
from error_exception import *

#######################################################################################################
#                                                                                                     #
#                                               PARAMETERS                                            #
#                                                                                                     #
#######################################################################################################

# TEMPERATURE_LIST = (0 TEMPERATURA_INICIAL, 1 TEMPERATURA_ATUAL, 2 ALPHA, 3 COOLING_OPTION)
def initialize_parameters():
    global temperature_list
    initial_temperature = 0
    alpha = 0
    cooling_option = ''

    try:
        file = open('simulated_annealing_parameter.txt', 'r', encoding="utf-8")
    except:
        error_exception('ERRO: simulated_annealing.py - ARQUIVO simulated_annealing_parameter.txt NÃO ENCONTRADO')
    lines = file.read().splitlines()
    for line in lines:
        if ((str(line).strip()) or (line[0] == '#')): # IGNORA SE VAZIO OU COMENTARIO
            parameter = line.split(" ", 1)
            if (parameter[0] == 'INITIAL_TEMPERATURE'):
                initial_temperature = float(parameter[1])
            elif (parameter[0] == 'COOLING_SCHEDULE'):
                cooling_option = parameter[1]
            elif (parameter[0] == 'ALPHA'):
                alpha = float(parameter[1])
    file.close()

    temperature = initial_temperature
    temperature_list = [initial_temperature, temperature, alpha, cooling_option]

#######################################################################################################
#                                                                                                     #
#                                               TEMPERATURE                                           #
#                                                                                                     #
#######################################################################################################

def cooling_scheme():
    global temperature_list
    cooling_options[temperature_list[3]]()

def geometric():
    global temperature_list
    temperature_list[1] = temperature_list[2] * temperature_list[1]

#######################################################################################################
#                                                                                                     #
#                                                 MAIN                                                #
#                                                                                                     #
#######################################################################################################

# CONSTANTES
cooling_options = {'GEOMETRIC': geometric}

initialize_parameters()
while (temperature_list[1] > 10):
    cooling_scheme()
    print(temperature_list[1])

card_dict, store_dict, content_table = run_input_reformat('1', 'steste.csv')
print(card_dict)
print(store_dict)
print(content_table)
print('SIMULATED ANNEALING INICIADO... FIM')

















"""
Select a starting solution x in D
Update set M of potentially efficient solutions with x
T:=To
repeat
    Construct Y in V(x)
    Update set M of potentially efficient solutions with y
    x := y (accept y) with probability p(x,y, T,A)
    if the conditions of changing the temperature are fulfilled then
        decrease T
until the stop conditions are fulfilled
"""