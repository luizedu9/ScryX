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
import copy
import sys
import math

from input_reformat import *
from error_exception import *

#####################################################################################################################
#                                                                                                                   #
#                                                        PARAMETERS                                                 #
#                                                                                                                   #
#####################################################################################################################

# TEMPERATURE_LIST = (0 TEMPERATURA_INICIAL, 1 TEMPERATURA_ATUAL, 2 ALPHA, 3 COOLING_OPTION, 4 FINAL_TEMPERATURE, 5 REHEAT)
def initialize_parameters():
    global temperature_list
    global roulette_option
    global acceptance_option
    global weight_list
    initial_temperature = 0
    alpha = 0
    cooling_option = ''
    final_temperature = 0
    reheat = 0
    roulette_option = ''
    acceptance_option = ''
    weight_list = []

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
            elif (parameter[0] == 'REHEAT'):
                reheat = int(parameter[1])
            elif (parameter[0] == 'ROULETTE_OPTION'):
                roulette_option = parameter[1]
            elif (parameter[0] == 'ACCEPTANCE_OPTION'):
                acceptance_option = parameter[1]
            elif ((parameter[0] == 'LAMBDA1') or (parameter[0] == 'LAMBDA2')):
                weight_list.append(float(parameter[1]))
    file.close()

    temperature = initial_temperature
    temperature_list = [initial_temperature, temperature, alpha, cooling_option, final_temperature, reheat]

#####################################################################################################################
#                                                                                                                   #
#                                                      TEMPERATURE                                                  #
#                                                                                                                   #
#####################################################################################################################

def cooling_scheme():
    global temperature_list
    cooling_options[temperature_list[3]]()

def cooling_geometric():
    global temperature_list
    temperature_list[1] = temperature_list[2] * temperature_list[1]

#####################################################################################################################
#                                                                                                                   #
#                                                     ROULETTE WHEEL                                                #
#                                                                                                                   #
#####################################################################################################################

# A ROLETA É UTILIZADA PARA DEFINIR A PROBABILIDADE DE CADA LOJA SER ESCOLHIDA PELA HEURISTICA
# NOTE QUE PARA CADA CARTA É NECESSARIO UMA ROLETA. SENDO ASSIM, EXISTIRA UMA LISTA COM N ELEMENTOS
# SENDO N O NUMERO DE CARTAS.
# roulette_values = (menor valor, maior valor, id da carta)

def roulette_wheel(card, exception):
    # EXCEPTION É A LOJA QUE JA ESTÁ SENDO USADA
    global roulette_values
    rand = random.uniform(0.00000001, 100)
    boolean = False
    if ((len(roulette_values[card]) == 1) and (exception != '')):
        return(None)
    # PARA CADA FATIA DA ROLETA NA POSIÇÃO DA CARTA, ENCONTRE A LOJA CORRESPONDENTE AO RANDOM 
    for value in roulette_values[card]:
        if (((rand > value[0]) and (rand <= value[1])) or (boolean == True)):
            if (value[2] == exception):
                boolean = True
            else:
                return(value[2])
    return(roulette_values[card][0][2])

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

#####################################################################################################################
#                                                                                                                   #
#                                                  ACCEPTANCE CRITERIA                                              #
#                                                                                                                   #
#####################################################################################################################

# OS CRITERIOS DE ACEITAÇÃO C, SL E W SE ENCONTRAM NO ARTIGO DO CZYZAK ET AL.
def rule_c(x, y):
    global temperature_list
    global weight_list
    result = 0
    for i in range(len(weight_list)):
        temp = (weight_list[i] * ((fitness_options[i](x) - fitness_options[i](y)) / temperature_list[1]))
        if (temp > result):
            result = temp
    result = math.exp(result)
    if (result >= 1):
        return(1)
    return(result)

def rule_sl(x, y):
    global temperature_list
    global weight_list
    result = 0
    for i in range(len(weight_list)):
        result += weight_list[i] * ((fitness_options[i](x) - fitness_options[i](y)) / temperature_list[1])
    result = math.exp(result)
    if (result >= 1):
        return(1)
    return(result)

def rule_w(x, y):
    global temperature_list
    global weight_list
    result = 1
    for i in range(len(weight_list)):
        temp = (weight_list[i] * ((fitness_options[i](x) - fitness_options[i](y)) / temperature_list[1]))
        if (temp < result):
            result = temp
    result = math.exp(result)
    if (result >= 1):
        return(1)
    return(result)

#####################################################################################################################
#                                                                                                                   #
#                                                      FIRST SOLUTION                                               #
#                                                                                                                   #
#####################################################################################################################

def init_first_solution(empty_table):
    global total_card_quantity
    total_card_quantity = 0
    result_table = copy.deepcopy(empty_table)
    # PARA CADA CARTA, ESCOLHA UMA OU MAIS LOJAS PARA SE COMPRAR
    for card in card_dict.items():
        result_table = set_quantity(result_table, card)
        total_card_quantity += card[1][1]
    return(result_table)

#####################################################################################################################
#                                                                                                                   #
#                                                 OPERATIONS RESULT TABLE                                           #
#                                                                                                                   #
#####################################################################################################################

# ESTE SWAP ZERA TODA A LINHA DA CARTA, E ESCOLHE UMA OU MAIS POSIÇÕES NOVAS PARA A QUANTIDADE
def swap_change_all(result_table, card):
    return(set_quantity(result_table, card))

##### PROVAVELMENTE ERRADO CONFERIR, ACHO QUE TA DEIXANDO PASSAR PRA LOJA DESTINO MAIS CARTAS QUE TEM, ACHO
##### VARIAVEL CARD DO PARAMETRO DIFERENTE DO OUTRO SWAP, ESSE CARD É APENAS O ID, NO OUTRO É A TUPLA (ID, (NOME, QUANTIDADE))

# ESTE SWAP ESCOLHE UMA POSIÇÃO DA MATRIZ E MUDA A QUANTIDADE QUE ESTÁ LA PARA OUTRA POSIÇÃO, SENDO QUE SE NÃO
# OUVER ESPAÇO PARA TODAS AS CARTAS NA NOVA POSIÇÃO, ALGUMAS FICARÃO NA POSIÇÃO ORIGINAL
def swap_change_one(result_table, card):
    store_destination = roulette_wheel(card, store_origin)
    quantity_origin = result_table[card][store_origin]
    quantity_destination = result_table[card][store_destination]
    # will_stay É A QUANTIDADE DE CARTAS QUE NÃO IRÃO MUDAR DE LOJA
    will_stay = quantity_origin - (card_dict[card][1] - quantity_destination)
    # SE will_stay É MAIOR OU IGUAL A ZERO, ENTÃO POSIÇÃO ORIGEM RECEBE A QUANTIDADE DE CARTAS QUE 
    # IRÃO FICAR E O RESTANTE VAI PARA A POSIÇÃO DESTINO 
    if (will_stay >= 0):
        result_table[card][store_origin] = will_stay
        result_table[card][store_destination] += quantity_origin - will_stay
    # SE NÃO OUVER CARTAS SUFICIENTES PARA FICAR, PASSA TUDO PARA A OUTRA POSIÇÃO
    else:
        result_table[card][store_origin] = 0
        result_table[card][store_destination] += quantity_origin

# ZERA A LINHA DE QUANTIDADE E COLOCA A QUANTIDADE EM NOVAS POSIÇÕES
def set_quantity(result_table, card):
    quantity_remnant = card[1][1]
    store = ''
    stores = []
    # ZERA QUALQUER VALORES ANTERIORES
    for i in range(len(result_table[card[0]])):
        result_table[card[0]][i] = 0
    # ENQUANTO QUANTIDADE DE CARTAS NÃO ACABAR, COLOCA EM NOVAS LOJAS
    while (quantity_remnant > 0):
        store = roulette_wheel(card[0], store)
        if (store == None):
            break
        # SE NÃO É NENHUMA DAS LOJAS JÁ UTILIZADAS
        if not(store in stores):
            stores.append(store)
            # SE TIVER ACABADO A QUANTIDADE DE CARTAS, BREAK
            if (get_quantity_content(content_table[card[0]][store]) >= quantity_remnant):
                result_table[card[0]][store] = quantity_remnant
                break
            # SE NÃO CONTINUA ATÉ QUE TODAS AS CARTAS TENHAM SIDO ALOCADAS
            else:
                result_table[card[0]][store] = get_quantity_content(content_table[card[0]][store])
                quantity_remnant -= result_table[card[0]][store]
    return(result_table)

# DADO UMA TABELA DE RESULTADOS, SOMA O VALOR TOTAL
def get_fitness_price(result_table):
    price = 0
    for i in range(len(result_table)):
        for j in range(len(result_table[i])):
            if (result_table[i][j] != 0):
                price += get_price_content(result_table, i, j)
    return(price)

# O FITNESS DE QUANTIDADE CONTA QUANTAS CARTAS ESTÃO FALTANDO. OU SEJA, QUANTO MAIOR O RESULTADO, MAIS CARTAS ESTÃO FALTANDO
def get_fitness_quantity(result_table):
    global total_card_quantity
    quantity = 0
    for i in range(len(result_table)):
        for j in range(len(result_table[i])):
            quantity += result_table[i][j]
    return(total_card_quantity - quantity)

# DADO UMA TABELA DE RESULTADOS, SOMA O VALOR TOTAL
def get_quantity(result_table):
    quantity = 0
    for i in range(len(result_table)):
        for j in range(len(result_table[i])):
            quantity += result_table[i][j]
    return(quantity)

#####################################################################################################################
#                                                                                                                   #
#                                                 OPERATIONS CONTENT TABLE                                          #
#                                                                                                                   #
#####################################################################################################################

# ESSA FUNÇÃO RETORNA UMA LISTA DE TUPLA DE QUANTIDADE E PREÇO RELATIVO A QUANTIDADE DE CARTAS PASSADAS POR PARAMETRO
def set_quantity_content(quantity, field):
    # FIELD É O CAMPO DA MATRIZ QUE CONTEM UMA LISTA DE TUPLAS DE (QUANTIDADE, PREÇO)
    quantity_list_result = []
    for tuplex in field:
        if (tuplex[0] >= quantity):
            quantity_list_result.append((quantity, tuplex[1]))
            return(quantity_list_result)
        else:
            quantity_list_result.append((tuplex[0], tuplex[1]))
            quantity -= tuplex[0]
    return(quantity_list_result)

def get_quantity_content(field):
    quantity = 0
    for tuplex in field:
        quantity += tuplex[0]
    return(quantity)

def get_price_content(result_table, i, j):
    price = 0
    quantity = result_table[i][j]
    for tuplex in content_table[i][j]:
        if (quantity <= tuplex[0]):
            price += quantity * tuplex[1]
        else:
            price += tuplex[0] * tuplex[1]
            quantity -= tuplex[0]
    return(price)

#####################################################################################################################
#                                                                                                                   #
#                                                         MAIN                                                      #
#                                                                                                                   #
#####################################################################################################################

# CONSTANTES
cooling_options = {'GEOMETRIC': cooling_geometric}
roulette_options = {'UNIFORM': roulette_uniform, 'QUANTITY': roulette_quantity, 'PRICE': roulette_price, 'BOTH': roulette_both}
acceptance_options = {'C': rule_c, 'SL': rule_sl, 'W': rule_w}
fitness_options = {0: get_fitness_price, 1: get_fitness_quantity}

print('|---------------------------------------------------------------------------|')
print('|------------------------SIMULATED ANNEALING INICIADO-----------------------|')
print('|---------------------------------------------------------------------------|')
print()

# INICIALIZA OS PARAMETROS DO "simulated_annealing_parameter.txt"
initialize_parameters()
# INICIALIZA AS ESTRUTURAS DE DADOS DO PROGRAMA
card_dict, store_dict, content_table, empty_table = run_input_reformat(sys.argv[1], sys.argv[2])

# INICIALIZA A ROLETA
init_roulette_wheel()
# GERA UMA SOLUÇÃO INICIAL
solutions = []
solutions.append(init_first_solution(empty_table))
solution = copy.deepcopy(solutions[0])

#################################################
#                                               #
#                   EXECUTION                   #
#                                               #
#################################################


#### ROLETA VICIADA
#### FRETE 

cont = 0
melhor = 100000

for i in range(temperature_list[5]):
    temperature_list[1] = temperature_list[0]
    # ENQUANTO TEMPERATURA ESTIVER MAIOR QUE TEMPERATURA_FIM
    while (temperature_list[1] > temperature_list[4]):
        # GERA UMA NOVA SOLUÇÃO TROCANDO A QUANTIDADE DE DETERMINADA CARTA PARA NOVA LOJA
        for card in card_dict.items():
            #print(solution)
            new_solution = copy.deepcopy(swap_change_all(solution, card))
            #print(new_solution)
            acceptance = acceptance_options[acceptance_option](solution, new_solution)
            #print(solution)
            #print(new_solution)
            if (random.uniform(0, 1) <= acceptance):
                solution = new_solution
                #print('#####' + str(acceptance))
                #solutions.append(new_solution)
                if (get_fitness_price(new_solution) < melhor):
                    melhor = get_fitness_price(new_solution)
                    print('----------------' + str(melhor))
                    print(new_solution)
        cooling_scheme()
        print(temperature_list[1])
        cont += 1

print('Resultado' + str(melhor))

"""
print(cont)

melhor = 1000000
for i in solutions:
    temp = get_fitness_price(i)
    if (temp < melhor):
        melhor = temp
print(temp)
"""

print()
print('|---------------------------------------------------------------------------|')
print('|------------------------------------FIM------------------------------------|')
print('|---------------------------------------------------------------------------|')

"""
*Select a starting solution x in D
*Update set M of potentially efficient solutions with x
*T:=To
*repeat
    Construct Y in V(x)
    Update set M of potentially efficient solutions with y
    *x := y (accept y) with probability p(x,y, T,A)
    if the conditions of changing the temperature are fulfilled then
        *decrease T
*until the stop conditions are fulfilled
"""
"""
def init_first_solution(empty_table):
    global total_card_quantity
    total_card_quantity = 0
    result_table = copy.deepcopy(empty_table)
    for card, value in card_dict.items():
        quantity_remnant = value[1]
        store = ''
        stores = []
        total_card_quantity += value[1]
        # ENQUANTO QUANTIDADE DE CARTAS NÃO ACABAR, COLOCA EM NOVAS LOJAS
        while (quantity_remnant > 0):
            store = roulette_wheel(card, store)
            if (store == None):
                break
            # SE NÃO É NENHUMA DAS LOJAS JÁ UTILIZADAS
            if not(store in stores):
                stores.append(store)
                # SE TIVER ACABADO A QUANTIDADE DE CARTAS, BREAK
                if (get_quantity_content(content_table[card][store]) >= quantity_remnant):
                    result_table[card][store] = quantity_remnant
                    break
                # SE NÃO CONTINUA ATÉ QUE TODAS AS CARTAS TENHAM SIDO ALOCADAS
                else:
                    result_table[card][store] = get_quantity_content(content_table[card][store])
                    quantity_remnant -= result_table[card][store]
    return(result_table)
"""