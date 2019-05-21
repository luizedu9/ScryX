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

import random

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
    global roulette_option
    initial_temperature = 0
    alpha = 0
    cooling_option = ''
    final_temperature = 0
    roulette_option = ''

    try:
        file = open('simulated_annealing_parameter.txt', 'r', encoding="utf-8")
    except:
        error_exception('ERRO: simulated_annealing.py - ARQUIVO simulated_annealing_parameter.txt NÃO ENCONTRADO')
    lines = file.read().splitlines()
    for line in lines:
        if not((str(line).strip()) and (line[0] == '#')): # IGNORA SE VAZIO OU COMENTARIO
            parameter = line.split(" ", 1)
            if (parameter[0] == 'INITIAL_TEMPERATURE'):
                initial_temperature = float(parameter[1])
            elif (parameter[0] == 'COOLING_SCHEDULE'):
                cooling_option = parameter[1]
            elif (parameter[0] == 'ALPHA'):
                alpha = float(parameter[1])
            elif (parameter[0] == 'FINAL_TEMPERATURE'):
                final_temperature = float(parameter[1])
            elif (parameter[0] == 'ROULETTE_OPTION'):
                roulette_option = parameter[1]
    file.close()

    temperature = initial_temperature
    temperature_list = [initial_temperature, temperature, alpha, cooling_option, final_temperature]

#######################################################################################################
#                                                                                                     #
#                                               TEMPERATURE                                           #
#                                                                                                     #
#######################################################################################################

def cooling_scheme():
    global temperature_list
    cooling_options[temperature_list[3]]()

def cooling_geometric():
    global temperature_list
    temperature_list[1] = temperature_list[2] * temperature_list[1]

#######################################################################################################
#                                                                                                     #
#                                             ROULETTE WHEEL                                          #
#                                                                                                     #
#######################################################################################################

# A ROLETA É UTILIZADA PARA DEFINIR A PROBABILIDADE DE CADA LOJA SER ESCOLHIDA PELA HEURISTICA
# NOTE QUE PARA CADA CARTA É NECESSARIO UMA ROLETA. SENDO ASSIM, EXISTIRA UMA LISTA COM N ELEMENTOS
# SENDO N O NUMERO DE CARTAS.
# roulette_values = (menor valor, maior valor, id da carta)

def roulette_wheel(card):
    global roulette_values
    rand = random.uniform(0.00000001, 100)
    # PARA CADA FATIA DA ROLETA NA POSIÇÃO DA CARTA, ENCONTRE A LOJA CORRESPONDENTE AO RANDOM 
    for value in roulette_values[card]:
        if ((rand > value[0]) and (rand <= value[1])):
            return(value[2])

def init_roulette_wheel():
    global roulette_option
    roulette_options[roulette_option]()

def roulette_uniform():
    global roulette_values
    roulette_values = []
    # PARA CADA CARTA...
    for i in range(len(card_dict)):
        roulette_values.append([])
        # ...VERIFICA QUANTAS LOJAS A POSSUI...
        store_temp = []
        for j in range(len(content_table[i])):
            # SE CAMPO DA MATRIZ NÃO ESTA VAZIO
            if (content_table[i][j]):
                store_temp.append(j)
        # ...E ADICIONA FATIAS DA ROLETA PARA ESSA LOJA 
        percent = 100 / len(store_temp)
        rangex = 0
        rangey = 0
        for store in store_temp:
            rangey += percent
            roulette_values[i].append((float('%.2f'%rangex), float('%.2f'%rangey), store))
            rangex = rangey

# TODO
def roulette_quantity():
    global roulette_values
    pass

# TODO
def roulette_price():
    global roulette_values
    pass

# TODO
def roulette_both():
    global roulette_values
    pass

#######################################################################################################
#                                                                                                     #
#                                                 MAIN                                                #
#                                                                                                     #
#######################################################################################################

# CONSTANTES
cooling_options = {'GEOMETRIC': cooling_geometric}
roulette_options = {'UNIFORM': roulette_uniform, 'QUANTITY': roulette_quantity, 'PRICE': roulette_price, 'BOTH': roulette_both}

print('SIMULATED ANNEALING INICIADO...')
initialize_parameters()
card_dict, store_dict, content_table = run_input_reformat('1', 'steste.csv')
init_roulette_wheel()

while (temperature_list[1] > temperature_list[4]):
    cooling_scheme()
    valor = roulette_wheel(0)
    print(temperature_list[1])

print('***** FIM *****')

















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