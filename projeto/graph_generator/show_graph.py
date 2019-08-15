# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   show.graph.py:
#   Este modulo tem como objetivo gerar graficos dos resultados a partir de um arquivo CSV
#
#   python3 show_graph.py result.csv nome_saida

import matplotlib.pyplot as plt
import csv
import sys

with open(sys.argv[1], 'r') as file:
    reader = csv.reader(file)
    result_list = list(reader)

plt.xlabel('Lojas')
plt.ylabel('Preço')
plt.title(sys.argv[1])

# PARA ENCONTRAR O MAIOR E MENOR VALOR DE CADA EIXO PARA ENCONTRAR A ESCALA APROPRIADA
maiorx = 0
maiory = 0
menorx = 999999999
menory = 999999999
i = 1
while (i < len(result_list)):
    if (float(result_list[i][0]) < menory):
        menory = float(result_list[i][0])
    if (float(result_list[i][1]) < menorx):
        menorx = float(result_list[i][1])
    if (float(result_list[i][0]) > maiory):
        maiory = float(result_list[i][0])
    if (float(result_list[i][1]) > maiorx):
        maiorx = float(result_list[i][1])
    i += 1
maiorx += 1 
maiory = int(maiory + (maiory * 0.2))
menorx -= 1
menory = int(menory - (menory * 0.2))

# DEFINE ESCALAS
plt.axis([menorx, maiorx, menory, maiory])

# PLOTA SOLUÇÃO DA LIGAMAGIC EM VERMELHO
plt.plot(float(result_list[1][1]), float(result_list[1][0]), 'ro')

axisx = []
axisy = []
i = 2
while (i < len(result_list)): 
    axisx.append(float(result_list[i][1]))
    axisy.append(float(result_list[i][0]))
    i += 1

# PLOTA RESTANTE DAS SOLUÇÕES DO SA
plt.plot(axisx, axisy, 'go')
plt.plot(axisx, axisy, 'b-')

plt.savefig(sys.argv[2] + '.png')