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
import threading
from multiprocessing import Process, Array, Queue
import time
import numpy as np

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
    global n_thread
    global n_solution_pool
    global pareto_timeout
    initial_temperature = 0
    alpha = 0
    cooling_option = ''
    final_temperature = 0
    reheat = 0
    roulette_option = ''
    acceptance_option = ''
    weight_list = []
    n_thread = 1
    n_solution_pool = 0
    pareto_timeout = 0

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
            elif ((parameter[0] == 'LAMBDA1') or (parameter[0] == 'LAMBDA2') or (parameter[0] == 'LAMBDA3')):
                weight_list.append(float(parameter[1]))
            elif (parameter[0] == 'N_THREAD'):
                n_thread = int(parameter[1])
            elif (parameter[0] == 'N_SOLUTION_POOL'):
                n_solution_pool = int(parameter[1])
            elif (parameter[0] == 'PARETO_TIMEOUT'):
                pareto_timeout = int(parameter[1])
    file.close()

    temperature = initial_temperature
    temperature_list = [initial_temperature, temperature, alpha, cooling_option, final_temperature, reheat]

def initialize_total_card_quantity():
    global total_card_quantity
    total_card_quantity = 0
    for card in card_dict.items():
        total_card_quantity += card[1][1]

#####################################################################################################################
#                                                                                                                   #
#                                                      TEMPERATURE                                                  #
#                                                                                                                   #
#####################################################################################################################

def cooling_scheme(current_temperature):
    global temperature_list
    return(cooling_options[temperature_list[3]](current_temperature))

def cooling_geometric(current_temperature):
    global temperature_list
    return(temperature_list[2] * current_temperature)

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

def initialize_roulette_wheel():
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
def rule_c(x, y, current_temperature):
    global temperature_list
    global weight_list
    result = 0
    for i in range(len(weight_list)):
        temp = weight_list[i] * ((x[i+1] - y[i+1]) / current_temperature)
        if (temp > result):
            result = temp
    result = math.exp(result)
    if (result >= 1):
        return(1)
    return(result)

def rule_sl(x, y, current_temperature):
    global temperature_list
    global weight_list
    result = 0
    for i in range(len(weight_list)):
        result += weight_list[i] * ((x[i+1] - y[i+1]) / current_temperature)
    result = math.exp(result)
    if (result >= 1):
        return(1)
    return(result)

def rule_w(x, y, current_temperature):
    global temperature_list
    global weight_list
    result = 1
    for i in range(len(weight_list)):
        temp = weight_list[i] * ((x[i+1] - y[i+1]) / current_temperature)
        if (temp < result):
            result = temp
    result = math.exp(result)
    if (result >= 1):
        return(1)
    return(result)

#####################################################################################################################
#                                                                                                                   #
#                                                          PARETO                                                   #
#                                                                                                                   #
#####################################################################################################################

# BASEADO EM is_pareto_efficient. ACESSADO EM:
#   <https://stackoverflow.com/questions/32791911/fast-calculation-of-pareto-front-in-python>
# costs É UM NUMPY ARRAY COM OS CUSTOS DE CADA OBJETIVO
def pareto(costs):
    is_efficient = np.arange(costs.shape[0])
    n_points = costs.shape[0]
    next_point_index = 0
    while (next_point_index < len(costs)):
        nondominated_point_mask = np.any(costs < costs[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        is_efficient = is_efficient[nondominated_point_mask]
        costs = costs[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index]) + 1
    return(is_efficient)

#####################################################################################################################
#                                                                                                                   #
#                                                      FIRST SOLUTION                                               #
#                                                                                                                   #
#####################################################################################################################

def init_first_solution(empty_table):
    result_table = copy.deepcopy(empty_table)
    # PARA CADA CARTA, ESCOLHA UMA OU MAIS LOJAS PARA SE COMPRAR
    for card in card_dict.items():
        result_table = set_quantity(result_table, card)
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

# RETORNA UMA TUPLA COM OS FITNESS DOS OBJETIVOS 
def get_fitness(result_table):
    global total_card_quantity
    quantity = 0
    price = 0
    stores = set()
    for i in range(len(result_table)):
        for j in range(len(result_table[i])):
            if (result_table[i][j] != 0):
                price += get_price_content(result_table, i, j)
                quantity += result_table[i][j]
                stores.add(store_dict[j])
    return( (price, (total_card_quantity - quantity), len(stores)))            

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
#                                                       THREADS                                                     #
#                                                                                                                   #
#####################################################################################################################

# ESSA THREAD PROCURA POR CANDIDATOS A SOLUÇÃO
def execute_thread(solution_deliver, id_thread):

    print('|-----------------------------THREAD ' +  str (id_thread) + ' INICIADA-----------------------------|')

    # GERA UMA SOLUÇÃO INICIAL - TUPLA DE (0 CONTEUDO DA SOLUÇÃO, 1 OBJETIVO1, 2 OBJETIVO2, ... )
    result_table = [list(x) for x in init_first_solution(empty_table)]
    objectives = get_fitness(result_table)
    objective1 = objectives[0]
    objective2 = objectives[1]
    objective3 = objectives[2]
    solution = (result_table, objective1, objective2, objective3)

    # REPITA N VEZES, SENDO N O NUMERO DE REAQUECIMENTOS DO SISTEMA
    for i in range(temperature_list[5]):
        current_temperature = temperature_list[0]
        # ENQUANTO TEMPERATURA ESTIVER MAIOR QUE TEMPERATURA_FIM
        while ((current_temperature > temperature_list[4])):
            # GERA UMA NOVA SOLUÇÃO TROCANDO A QUANTIDADE DE DETERMINADA CARTA PARA NOVA LOJA
            for card in card_dict.items():
                result_table = swap_change_all([list(x) for x in solution[0]], card)
                objectives = get_fitness(result_table)
                objective1 = objectives[0]
                objective2 = objectives[1]
                objective3 = objectives[2]
                new_solution = (result_table, objective1, objective2, objective3)                
                if (random.uniform(0, 1) <= acceptance_options[acceptance_option](solution, new_solution, current_temperature)):
                    solution = new_solution
                    # ENTREGA A SOLUÇÃO PARA A THREAD RESPONSAVEL
                    solution_deliver.put(solution)
                    if (new_solution[1] < melhor[id_thread]):
                        melhor[id_thread] = new_solution[1]
                        print('----------------' + str("%.2f" % melhor[id_thread]) + '----------------------------' + str(id_thread))
                    
            current_temperature = cooling_scheme(current_temperature)

    print('|----------------------------THREAD ' +  str (id_thread) + ' FINALIZADA----------------------------|')

# ESSA THREAD DADO UM CONJUNTO DE CANDIDATOS A SOLUÇÕES ENCONTRA A FRONTEIRA DE PARETO
def pareto_thread(solution_deliver):
    global solutions
    global n_solution_pool
    global pareto_timeout
    global weight_list

    print('|---------------------------THREAD PARETO INICIADA--------------------------|')
    
    solutions = []

    try:
        # Recebe possiveis soluções, quando recebe o suficiente, calcula a Fronteira de Pareto
        while (True):
            # SE NÃO RECEBER NADA EM pareto_timeout, EXECUTA O except PARA FINALIZAR A THREAD
            solutions.append(solution_deliver.get(timeout=pareto_timeout))
            if (len(solutions) >= n_solution_pool):
                first_pass = True
                for solution in solutions:
                    if (first_pass):
                        solutions_calculated = np.array([(solution[1], solution[2], solution[3])])
                        first_pass = False
                    else:
                        solutions_calculated = np.append(solutions_calculated, [(solution[1], solution[2], solution[3])], axis=0)
                new_solutions_index = pareto(solutions_calculated)
                new_solutions = []
                for index in new_solutions_index:
                    result_table = [list(x) for x in solutions[index][0]]
                    new_solutions.append( (result_table, solutions[index][1], solutions[index][2], solutions[index][3]) )
                solutions = new_solutions
                print('.')
    except:
        first_pass = True
        for solution in solutions:
            if (first_pass):
                solutions_calculated = np.array([(solution[1], solution[2], solution[3])])
                first_pass = False
            else:
                solutions_calculated = np.append(solutions_calculated, [(solution[1], solution[2], solution[3])], axis=0)
        new_solutions_index = pareto(solutions_calculated)
        new_solutions = []
        for index in new_solutions_index:
            result_table = [list(x) for x in solutions[index][0]]
            new_solutions.append( (result_table, solutions[index][1], solutions[index][2], solutions[index][3]) )
        solutions = new_solutions
        print(solutions[0])
        print('RESULTADO ' + str(solutions[0][1]))
    
    print('|-------------------------THREAD PARETO FINALIZADA--------------------------|')

def initialize_thread():
    global solution_deliver
    threads = list()
    solution_deliver = Queue()

    # INICIALIZA THREAD QUE CALCULA AS SOLUÇÕES FINAIS
    solution_thread = Process(target=pareto_thread, args=(solution_deliver,))
    #solution_thread.daemon = True
    solution_thread.start()

    # INICIALIZA THREADS DE BUSCA DE SOLUÇÕES
    for index in range(n_thread):
        thread = Process(target=execute_thread, args=(solution_deliver, index,))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    return(threads, solution_thread)

def terminate_thread(threads, solution_thread):
    solution_thread.join()
    for index, thread in enumerate(threads):
        thread.join()
    #solution_thread.join()


#####################################################################################################################
#                                                                                                                   #
#                                                         MAIN                                                      #
#                                                                                                                   #
#####################################################################################################################

# CONSTANTES
cooling_options = {'GEOMETRIC': cooling_geometric}
roulette_options = {'UNIFORM': roulette_uniform, 'QUANTITY': roulette_quantity, 'PRICE': roulette_price, 'BOTH': roulette_both}
acceptance_options = {'C': rule_c, 'SL': rule_sl, 'W': rule_w}

print('|---------------------------------------------------------------------------|')
print('|------------------------SIMULATED ANNEALING INICIADO-----------------------|')
print('|---------------------------------------------------------------------------|')
print()

# INICIALIZA OS PARAMETROS DO "simulated_annealing_parameter.txt"
initialize_parameters()
# INICIALIZA AS ESTRUTURAS DE DADOS DO PROGRAMA
card_dict, store_dict, content_table, empty_table = run_input_reformat(sys.argv[1], sys.argv[2])
# INICIALIZA A ROLETA
initialize_roulette_wheel()
initialize_total_card_quantity()

#################################################
#                                               #
#                   EXECUTION                   #
#                                               #
#################################################


#### ROLETA VICIADA
#### SWAP CHANGE ONE
#### FRETE EM PREÇO, E NÃO COMO OBJETIVO

melhor = Array('d', range(n_thread))
for i in range(n_thread):
    melhor[i] = 100000

threads, solution_thread = initialize_thread()
terminate_thread(threads, solution_thread)

print()
print('|---------------------------------------------------------------------------|')
print('|------------------------------------FIM------------------------------------|')
print('|---------------------------------------------------------------------------|')