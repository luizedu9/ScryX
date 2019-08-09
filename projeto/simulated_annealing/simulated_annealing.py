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

import threading
from multiprocessing import Process, Array, Queue
import sys
import numpy as np
import pygmo as pg
import math
import time
import random
import logging
import copy

from input_reformat import *

#####################################################################################################################
#                                                                                                                   #
#                                                        PARAMETERS                                                 #
#                                                                                                                   #
#####################################################################################################################

def initialize_parameters():
    global TEMPERATURE_LIST
    global ROULETTE_OPTION
    global ACCEPTANCE_OPTION
    global WEIGHT_LIST
    global PRICE_INCREASE
    global QUANTITY_INCREASE
    global STORE_INCREASE
    global PERCENT_MISSING
    global N_THREAD
    global N_SOLUTION_POOL
    global RESULT
    INITITAL_TEMPERATURE = 0
    ALPHA = 0
    COOLING_OPTION = ''
    FINAL_TEMPERATURE = 0
    REHEAT = 0
    ROULETTE_OPTION = ''
    ACCEPTANCE_OPTION = ''
    WEIGHT_LIST = []
    PRICE_INCREASE = 0
    QUANTITY_INCREASE = 1
    STORE_INCREASE = 1
    PERCENT_MISSING = 100
    N_THREAD = 1
    N_SOLUTION_POOL = 0
    RESULT = ''

    try:
        file = open('simulated_annealing_parameter.txt', 'r', encoding="utf-8")
    except:
        logger.warning('ERRO: simulated_annealing.py - ARQUIVO simulated_annealing_parameter.txt NÃO ENCONTRADO')
        exit()
    lines = file.read().splitlines()
    for line in lines:
        if not((str(line).strip()) and (line[0] == '#')): # IGNORA SE VAZIO OU COMENTARIO
            parameter = line.split(" ", 1)
            if (parameter[0] == 'INITIAL_TEMPERATURE'):
                INITITAL_TEMPERATURE = float(parameter[1])
            elif (parameter[0] == 'COOLING_SCHEDULE'):
                COOLING_OPTION = parameter[1]
            elif (parameter[0] == 'ALPHA'):
                ALPHA = float(parameter[1])
            elif (parameter[0] == 'FINAL_TEMPERATURE'):
                FINAL_TEMPERATURE = float(parameter[1])
            elif (parameter[0] == 'REHEAT'):
                REHEAT = int(parameter[1])
            elif (parameter[0] == 'ROULETTE_OPTION'):
                ROULETTE_OPTION = parameter[1]
            elif (parameter[0] == 'ACCEPTANCE_OPTION'):
                ACCEPTANCE_OPTION = parameter[1]
            elif ((parameter[0] == 'LAMBDA1') or (parameter[0] == 'LAMBDA2') or (parameter[0] == 'LAMBDA3')):
                WEIGHT_LIST.append(float(parameter[1]))
            elif (parameter[0] == 'PRICE_INCREASE'):
                PRICE_INCREASE = int(parameter[1])
            elif (parameter[0] == 'QUANTITY_INCREASE'):
                QUANTITY_INCREASE = int(parameter[1])
            elif (parameter[0] == 'STORE_INCREASE'):
                STORE_INCREASE = int(parameter[1]) 
            elif (parameter[0] == 'PERCENT_MISSING'):
                PERCENT_MISSING = int(parameter[1])  
            elif (parameter[0] == 'N_THREAD'):
                N_THREAD = int(parameter[1])
            elif (parameter[0] == 'N_SOLUTION_POOL'):
                N_SOLUTION_POOL = int(parameter[1])
            elif (parameter[0] == 'RESULT'):
                RESULT = parameter[1]

    file.close()

    # TEMPERATURE_LIST = (0 TEMPERATURA_INICIAL, 1 TEMPERATURA_ATUAL, 2 ALPHA, 3 COOLING_OPTION, 4 FINAL_TEMPERATURE, 5 REHEAT)
    TEMPERATURE_LIST = [INITITAL_TEMPERATURE, INITITAL_TEMPERATURE, ALPHA, COOLING_OPTION, FINAL_TEMPERATURE, REHEAT]

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
    global TEMPERATURE_LIST
    return(cooling_options[TEMPERATURE_LIST[3]](current_temperature))

def cooling_geometric(current_temperature):
    global TEMPERATURE_LIST
    return(TEMPERATURE_LIST[2] * current_temperature)

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
    global ROULETTE_OPTION
    roulette_options[ROULETTE_OPTION]()

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

# ESSA ROLETA DEFINE UMA CHANCE MAIOR DE SER SELECIONADA PARA LOJAS QUE POSSUEM MAIS CARTAS
def roulette_quantity():
    global roulette_values
    roulette_values = []

    store_score = [] # NUMERO DE CARTAS TOTAL DE CADA LOJA
    for i in range(len(content_table[0])): # PASSA EM CADA LOJA
        store_score.append(0)
        for j in range(len(content_table)):
            temp = get_quantity_content(content_table[j][i]) # PASSA EM CADA CARTA
            if (temp > card_dict[j][1]):
                temp = card_dict[j][1]
            store_score[i] += temp
    # PARA CADA CARTA...
    for i in range(len(card_dict)):
        roulette_values.append([])
        # ...VERIFICA QUANTAS LOJAS A POSSUI...
        store_temp = []
        score_temp = 0
        for j in range(len(content_table[i])):
            # SE CAMPO DA MATRIZ NÃO ESTA VAZIO
            if (content_table[i][j]):
                store_temp.append(j)
                score_temp += store_score[j]
        # ...E ADICIONA FATIAS DA ROLETA PARA ESSA LOJA 
        rangex = 0
        rangey = 0
        for store in store_temp:
            percent = store_score[store] * 100 / score_temp
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
def rule_sl(x, y, current_temperature):
    global TEMPERATURE_LIST
    global WEIGHT_LIST
    result = 0
    for i in range(len(WEIGHT_LIST)):
        result += WEIGHT_LIST[i] * ((x[i+1] - y[i+1]) / current_temperature)
    try:
        result = math.exp(result)
    except:
        return(1)
    if (result >= 1):
        return(1)
    return(result)

def rule_w(x, y, current_temperature):
    global TEMPERATURE_LIST
    global WEIGHT_LIST
    result = 1
    for i in range(len(WEIGHT_LIST)):
        temp = WEIGHT_LIST[i] * ((x[i+1] - y[i+1]) / current_temperature)
        if (temp < result):
            result = temp
    try:
        result = math.exp(result)
    except:
        return(1)
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

def prepara_pareto(solutions):
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
    return(new_solutions)

#####################################################################################################################
#                                                                                                                   #
#                                                      FIRST SOLUTION                                               #
#                                                                                                                   #
#####################################################################################################################

def init_first_solution(empty_table):
    result_table = copy.deepcopy(empty_table)
    # PARA CADA CARTA, ESCOLHA UMA OU MAIS LOJAS PARA SE COMPRAR
    for card in card_dict.items():
        result_table = swap_change_all(result_table, card)
    return(result_table)

#####################################################################################################################
#                                                                                                                   #
#                                                 OPERATIONS CONTENT TABLE                                          #
#                                                                                                                   #
#####################################################################################################################

def get_quantity_content(field):
    quantity = 0
    for tuplex in field:
        quantity += tuplex[0]
    return(quantity)

def get_price_content(result_table, i, j):
    price = 0
    quantity = result_table[i][j]
    for tuplex in content_table[i][j]:
        if (tuplex[0] >= quantity):
            price += quantity * tuplex[1]
            break
        else:
            price += tuplex[0] * tuplex[1]
            quantity -= tuplex[0]
    return(price)

# RETORNA TODOS OS PREÇOS DE DETERMINADA CARTA EM DETERMINADA LOJA
def get_content(i, j):
    content = []
    try:
        for k in content_table[i][j]:
            content.append(k)
        return(content)
    except: # SIGNIFICA QUE ESSA LOJA NÃO POSSUI ESSA CARTA
        return(None)

#####################################################################################################################
#                                                                                                                   #
#                                                 OPERATIONS RESULT TABLE                                           #
#                                                                                                                   #
#####################################################################################################################

# ESTE SWAP ZERA TODA A LINHA DA CARTA, E ESCOLHE UMA OU MAIS POSIÇÕES NOVAS PARA A QUANTIDADE
def swap_change_all(result_table, card):
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

def set_quantity(result_table, card, store, value):
    result_table[card][store] = value
    return(result_table)

# RETORNA UMA TUPLA COM OS FITNESS DOS OBJETIVOS (COM INCREMENTADORES)
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
    return( (price + (len(stores) * PRICE_INCREASE), (total_card_quantity - quantity) * QUANTITY_INCREASE, len(stores) * STORE_INCREASE))

# RETORNA UMA TUPLA COM OS FITNESS DOS OBJETIVOS (SEM INCREMENTADORES)
def get_final_fitness(result_table):
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
    return( (price, (total_card_quantity - quantity), len(stores)) )

# ARMAZENA O INDEX DAS COLUNAS QUE POSSUEM CARTAS
def find_stores(result_table):
    stores = []
    for i in range(len(result_table[0])):
        for j in range(len(result_table)):
            if (result_table[j][i] != 0):
                stores.append(i)
                break
    return(stores)

# ARMAZENA O INDEX E A QUANTIDADE DAS COLUNAS QUE POSSUEM CARTAS { id : quantidade_cartas}
def find_quantity(result_table):
    dict_quantity = {}
    for i in range(len(result_table)):
        for j in range(len(result_table[0])):
            if (result_table[i][j] != 0):
                try:
                    dict_quantity[j] += result_table[i][j]
                except:
                    dict_quantity[j] = result_table[i][j]
    return(dict_quantity)

# CRIA UMA LISTA EM ORDEM CRESCENTE POR PREÇO DA CARTA 
def find_lesser(result_table, stores, card):
    sort_stores = []
    for store in stores:
        contents = get_content(card, store)
        if (contents != None):
            for content in contents:
                sort_stores.append( (store, content[0], float(content[1])) ) # ID LOJA, QUANTIDADE, PREÇO
    sort_stores.sort(key=lambda tup: float(tup[2]))
    return(sort_stores)

#####################################################################################################################
#                                                                                                                   #
#                                                   POST OPTIMIZATION                                               #
#                                                                                                                   #
#####################################################################################################################

# SOLUTION - TUPLA DE (0 CONTEUDO DA SOLUÇÃO, 1 OBJETIVO1, 2 OBJETIVO2, ... )
def post_optimization(solutions):

    # O METODO ESCOLHIDO PARA A PÓS OTIMIZAÇÃO É PRIMEIRAMENTE REALOCAR TODAS AS CARTAS UTILIZANDO O 
    # METODO GULOSO COM AS LOJAS PRE SELECIONADAS. DEPOIS REMOVER A LOJA COM MENOS QUANTITATIVO E 
    # TENTAR COLOCAR AS CARTAS NAS OUTRAS LOJAS DA SOLUÇÃO. ENQUANTO O RESULTADO ESTIVER MELHORANDO, 
    # CONTINUA REMOVENDO LOJAS.

    logger.info('|--------------------------PÓS OTIMIZAÇÃO CALCULANDO------------------------|')

    remove_list = [] # GUARDA AS SOLUÇÕES QUE FORAM DOMINADAS PARA SER APAGADAS NO FINAL DA EXECUÇÃO

    # PARA CADA SOLUÇÃO, TENTA CRIAR UMA NOVA
    i = 0
    while (i < len(solutions)):
        solution = solutions[i]
        
        # OTIMIZA SOLUÇÃO ATUAL UTILIZANDO O METODO GULOSO
        stores = find_stores(solution[0]) # ENCONTRA LOJAS QUE POSSUEM CARTAS

        result_table = greedy_method(stores) # USA O METODO GULOSO PARA REALOCAR AS CARTAS
        objective1, objective2, objective3 = get_fitness(result_table)
        solutions[i] = ( ([list(x) for x in result_table], objective1, objective2, objective3) )
        
        # REMOVE A LOJA COM MENOR QUANTIDADE DE CARTAS PARA TENTAR CRIAR UMA NOVA SOLUÇAO
        if (solution[3] != (1 * STORE_INCREASE)): # SE SOLUÇÃO TIVER MAIS DE UMA LOJA, CONTINUE   
            stores.remove(sorted(find_quantity(result_table).items(), key=lambda item: item[1])[0][0]) # REMOVE UMA LOJA
            result_table = greedy_method(stores) # RECRIA SOLUÇÃO
            objective1, objective2, objective3 = get_fitness(result_table)
            new_solution = ( (result_table, objective1, objective2, objective3) )
            if (pg.pareto_dominance([solution[1], solution[2], solution[3]], [new_solution[1], new_solution[2], solution[3]]) == False):
                solutions.append(new_solution)
            # SE A NOVA SOLUÇÃO DOMINA A ANTIGA E A QUANTIDADE DE CARTAS QUE FALTAM NÃO AUMENTAR, REMOVE SOLUÇÃO ANTIGA
            if (pg.pareto_dominance([new_solution[1], new_solution[2], solution[3]], [solution[1], solution[2], solution[3]]) and new_solution[3] <= solution[3]):
                remove_list.append(i)
        i += 1

    # REMOVE SOLUÇÕES QUE FORAM DOMINADAS
    if len(remove_list) > 0:
        remove_list.reverse()
        for i in remove_list:
            solutions.pop(i)

    # REMOVE SOLUÇÕES QUE QUANTIDADE DE CARTAS QUE FALTARAM PASSARAM DO LIMITE ESTABELECIDO
    total_cards = 0
    remove_list = []
    for key, value in card_dict.items():
        total_cards += value[1]
    for i in range(len(solutions)):
        if (solutions[i][2] / QUANTITY_INCREASE) > (total_cards * (PERCENT_MISSING * 0.01)):
            remove_list.append(i)
    if len(remove_list) > 0:
        remove_list.reverse()
        for i in remove_list:
            solutions.pop(i)
    
    return(solutions)

# REALOCA TODAS AS CARTAS NAS LOJAS SELECIONADAS
def greedy_method(stores):
    # O METODO GULOSO REMOVE TODAS AS CARTAS DE SUAS POSIÇÕES ATUAIS E RECOLOCA EM NOVAS POSIÇÕES
    # SEGUINDO SEMPRE O MENOR PREÇO. AS LOJAS CANDIDATAS A REALOCAÇÃO SERÃO APENAS AQUELAS SELECIONADAS
    # NA SOLUÇÃO DO SIMULATED ANNEALING.
    result_table = [list(x) for x in empty_table] # ZERA RESULT TABLE
    # PARA CADA CARTA, CRIA UMA LISTA ORDENADA POR PREÇO
    for card in range(len(result_table)): # PARA CADA CARTA, FAÇA
        sort_stores = find_lesser(result_table, stores, card) # CRIA UMA LISTA DE TUPLAS DE PREÇO EM ORDEM CRESCENTE
        quantity_remnant = card_dict[card][1] # QUANTIDADE DE CARTAS REQUERIDAS
        for store in sort_stores: # ENQUANTO NÃO ALOCAR TODAS AS UNIDADES DE UMA CARTA, REPITA 
            if (quantity_remnant == 0): # SE ACABOU A QUANTIDADE A COLOCAR, SAI DO LAÇO
                break
            # SE QUANTIDADE DA LOJA FOR MAIOR QUE QUANTIDADE A SER ALOCADA, ENTÃO ENCERRA O LOOP
            if (store[1] >= quantity_remnant):
                set_quantity(result_table, card, store[0], quantity_remnant + result_table[card][store[0]])
                break
            else:
                value = quantity_remnant - (quantity_remnant - store[1])
                set_quantity(result_table, card, store[0], result_table[card][store[0]] + value )
                quantity_remnant -= value
    return(result_table)

#####################################################################################################################
#                                                                                                                   #
#                                                       THREADS                                                     #
#                                                                                                                   #
#####################################################################################################################

# ESSA THREAD PROCURA POR CANDIDATOS A SOLUÇÃO
def execute_thread(solution_deliver, id_thread):

    global N_SOLUTION_POOL

    logger.info('|-----------------------------THREAD ' +  str (id_thread) + ' INICIADA-----------------------------|')

    # GERA UMA SOLUÇÃO INICIAL - TUPLA DE (0 CONTEUDO DA SOLUÇÃO, 1 OBJETIVO1, 2 OBJETIVO2, ... )
    result_table = [list(x) for x in init_first_solution(empty_table)]
    objectives = get_fitness(result_table)
    objective1, objective2, objective3 = objectives[0], objectives[1], objectives[2]
    solution = (result_table, objective1, objective2, objective3)
    solutions = []

    # CONTA QUANTAS ITERAÇÕES O SIMULATED ANNEALING TERÁ
    ITERATION = 0
    progress = 0
    if (id_thread == 0):
        for i in range(TEMPERATURE_LIST[5]):
            current_temperature = TEMPERATURE_LIST[0]
            while ((current_temperature > TEMPERATURE_LIST[4])):
                ITERATION += 1
                current_temperature = cooling_scheme(current_temperature)

    # REPITA N VEZES, SENDO N O NUMERO DE REAQUECIMENTOS DO SISTEMA
    for i in range(TEMPERATURE_LIST[5]):
        
        current_temperature = TEMPERATURE_LIST[0]
        # ENQUANTO TEMPERATURA ESTIVER MAIOR QUE TEMPERATURA_FIM
        while ((current_temperature > TEMPERATURE_LIST[4])):
            if ((id_thread == 0) and (progress % 10 == 0)):
                logger.info("|----------------------- PROGRESSO SIMULATED ANNEALING ------------ " + str('%.2f'%((100 * progress) / ITERATION)) + " %")
            # GERA UMA NOVA SOLUÇÃO TROCANDO A QUANTIDADE DE DETERMINADA CARTA PARA NOVA LOJA
            for card in card_dict.items():
                result_table = swap_change_all([list(x) for x in solution[0]], card)
                objectives = get_fitness(result_table)
                objective1, objective2, objective3 = objectives[0], objectives[1], objectives[2]
                new_solution = (result_table, objective1, objective2, objective3)                
                if (random.uniform(0, 1) <= acceptance_options[ACCEPTANCE_OPTION](solution, new_solution, current_temperature)):
                    solution = new_solution
                    solutions.append(solution)
                    # ENTREGA A SOLUÇÃO PARA A THREAD RESPONSAVEL
                    if (len(solutions) >= N_SOLUTION_POOL):
                        solution_deliver.put(solutions)
                        solutions = []

            current_temperature = cooling_scheme(current_temperature)
            progress += 1

    solution_deliver.put(solutions)
    solution_deliver.put('thread_finished')
    logger.info('|----------------------------THREAD ' +  str (id_thread) + ' FINALIZADA----------------------------|')

# ESSA THREAD DADO UM CONJUNTO DE CANDIDATOS A SOLUÇÕES ENCONTRA A FRONTEIRA DE PARETO
def pareto_thread(solution_deliver, result_deliver):
    global solutions
    global N_SOLUTION_POOL
    global WEIGHT_LIST
    global N_THREAD

    logger.info('|---------------------------THREAD PARETO INICIADA--------------------------|')
    
    solutions = []
    n_thread_cont = N_THREAD

    # REPITA ATÉ QUE TODAS AS THREADS PRODUTORAS TENHAM SIDO FINALIZADAS
    while (n_thread_cont > 0):
        message = solution_deliver.get()
        if (message == 'thread_finished'):
            n_thread_cont -= 1
        else:
            solutions += message
            solutions = prepara_pareto(solutions)

    # ENTREGA SOLUÇÃO PARA O MAIN
    result_deliver.put(solutions)

    logger.info('|-------------------------THREAD PARETO FINALIZADA--------------------------|')

def initialize_thread():
    global solution_deliver
    global result_deliver
    threads = list()
    solution_deliver = Queue()
    result_deliver = Queue()

    # INICIALIZA THREAD QUE CALCULA AS SOLUÇÕES FINAIS
    solution_thread = Process(target=pareto_thread, args=(solution_deliver, result_deliver,))
    solution_thread.daemon = True
    solution_thread.start()

    # INICIALIZA THREADS DE BUSCA DE SOLUÇÕES
    for index in range(N_THREAD):
        thread = Process(target=execute_thread, args=(solution_deliver, index,))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    return(threads, solution_thread)

def terminate_thread(threads, solution_thread):
    for index, thread in enumerate(threads):
        thread.join()
    solutions = result_deliver.get()   
    solution_thread.join()

    logger.info("|----------------------- PROGRESSO SIMULATED ANNEALING ------------ 100.00 %")

    return(solutions)

#####################################################################################################################
#                                                                                                                   #
#                                                         MAIN                                                      #
#                                                                                                                   #
#####################################################################################################################

# CONSTANTES
cooling_options = {'GEOMETRIC': cooling_geometric}
roulette_options = {'UNIFORM': roulette_uniform, 'QUANTITY': roulette_quantity, 'PRICE': roulette_price, 'BOTH': roulette_both}
acceptance_options = {'SL': rule_sl, 'W': rule_w}

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

# INICIALIZA OS PARAMETROS DO "simulated_annealing_parameter.txt"
initialize_parameters()


if (RESULT == 'TERMINAL'):
    logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info('|---------------------------------------------------------------------------|')
logger.info('|------------------------SIMULATED ANNEALING INICIADO-----------------------|')
logger.info('|---------------------------------------------------------------------------|')
logger.info('')

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

# UTILIZA THREADS PARA ENCONTRAR A SOLUÇÃO
threads, solution_thread = initialize_thread()
solutions = terminate_thread(threads, solution_thread)

logger.info('')
logger.info('|---------------------------------------------------------------------------|')
logger.info('|-----------------------SIMULATED ANNEALING FINALIZADO----------------------|')
logger.info('|---------------------------------------------------------------------------|')
logger.info('')

logger.info('|---------------------------------------------------------------------------|')
logger.info('|---------------------------PÓS OTIMIZAÇÃO INICIADA-------------------------|')
logger.info('|---------------------------------------------------------------------------|')
logger.info('')

# UTILIZA UMA PÓS OTIMIZAÇÃO PARA TENTAR MELHORAR A SOLUÇÃO
solutions = post_optimization(solutions)
solutions = prepara_pareto(solutions)

logger.info('')
logger.info('|---------------------------------------------------------------------------|')
logger.info('|--------------------------PÓS OTIMIZAÇÃO FINALIZADA------------------------|')
logger.info('|---------------------------------------------------------------------------|')
logger.info('')

logger.info('RESULTADOS:')
if (RESULT == 'TERMINAL'):
    for solution in solutions:
        objectives = get_final_fitness(solution[0])
        logger.info('Valor: ' + str('%.2f'%objectives[0]) + ' / Lojas: ' + str(objectives[2]) + ' / Faltou: ' + str(objectives[1]))

elif (RESULT in 'CSV'):
    try:
        file = open('result' + sys.argv[2])
        file.close()
    except:
        with open('result' + sys.argv[2], 'w') as file:
            file.write('price\tstores\tmissing_cards\n')
    with open('result' + sys.argv[2], 'a+') as file:
        for solution in solutions:
            objectives = get_final_fitness(solution[0])
            file.write(str("%.2f"%objectives[0]) + '\t' + str(objectives[2]) + '\t' + str(objectives[1]) + '\n')
elif (RESULT == 'BD'):
    pass

logger.info('')
logger.info('|---------------------------------------------------------------------------|')
logger.info('|------------------------------------FIM------------------------------------|')
logger.info('|---------------------------------------------------------------------------|')