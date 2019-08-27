# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    

from flask import Flask, render_template,request,redirect,url_for
from pymongo import MongoClient, errors
import logging as log
from unicodedata import normalize
from bson import ObjectId
import os
import sys

from db_request import *
from functions import *
from user import User

#######################################################################################################
#                                                                                                     #
#                                                 INIT                                                #
#                                                                                                     #
#######################################################################################################

app = Flask(__name__)
title = "ScryX"
heading = "Prototipo"

user_logged = 1 # ********************************************************************

# CONECTA COM MONGODB
client = MongoClient('localhost', 27017)

# INICIA BD, SE NÃO EXISTIR, CRIA UM
if ('scryx' not in client.list_database_names()):
    db = client["scryx"]
    insert_current_queue(db)
    insert_length_queue(db)
else:
    db = client["scryx"]

todos = db.todo #REMOVER AHHHHHHHHHHHHHHHH ************************************************************************

try:
    client.server_info()
except:
    log.error('Can\'t connect to MongoDB')
    exit()

try: # CARREGA GERENCIADOR DE FILA
    current_queue = get_current_queue(db)
    length_queue = get_length_queue(db)
except:
    log.error('Can\'t read current_queue or length_queue')
    exit()

#######################################################################################################
#                                                                                                     #
#                                                  ROTE                                               #
#                                                                                                     #
#######################################################################################################

# CRIAÇÃO DE USUARIO
@app.route("/create_user", methods=['POST'])
def create_user ():
    if (request.values.get("password") != request.values.get("confirm_password")):
        return('ERRO') # **************************************************
    insert_user(db, User(
        request.values.get("username"),
        request.values.get("password"),
        request.values.get("name"),
        request.values.get("email"),
        request.values.get("birthdate"),
        request.values.get("gender")
        ))
    return redirect("/")

# CRIAÇÃO DE REQUISIÇÃO DE COTAÇÃO DE PREÇO
@app.route("/request_list", methods=['POST'])
def request_list():
    #try:
    error_list = register_request(db, request.values.get("card_list"), user_logged)
    if (error_list == []):
        return("Sucesso")
    else:
        return(str(error_list))
    #except:
    #    return('Houve um erro, tente mais tarde')

# INSERÇÃO DE CARTAS NO BANCO DE NOMES DE CARTAS
@app.route("/update_card_list", methods=['POST'])
def update_card_list():
    storage_cards(db, request.files['myfile'].read())
    return redirect("/")



#######################################################################################################
#                                                                                                     #
#                                                  EXEMPLO                                            #
#                                                                                                     #
#######################################################################################################
def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists ():
    #Display the all Tasks
    todos_l = todos.find()
    a1="active"
    return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks ():
    #Display the Uncompleted Tasks
    todos_l = todos.find({"done":"no"})
    a2="active"
    return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
    #Display the Completed Tasks
    todos_l = todos.find({"done":"yes"})
    a3="active"
    return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
    #Done-or-not ICON
    id=request.values.get("_id")
    task=todos.find({"_id":ObjectId(id)})
    if(task[0]["done"]=="yes"):
        todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
    else:
        todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
    redir=redirect_url()    

    return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
    #Adding a Task
    name=request.values.get("name")
    desc=request.values.get("desc")
    date=request.values.get("date")
    pr=request.values.get("pr")
    todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
    return redirect("/list")



@app.route("/remove")
def remove ():
    #Deleting a Task with various references
    key=request.values.get("_id")
    todos.remove({"_id":ObjectId(key)})
    return redirect("/")

@app.route("/update")
def update ():
    id=request.values.get("_id")
    task=todos.find({"_id":ObjectId(id)})
    return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
    #Updating a Task with various references
    name=request.values.get("name")
    desc=request.values.get("desc")
    date=request.values.get("date")
    pr=request.values.get("pr")
    id=request.values.get("_id")
    todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    #Searching a Task with various references

    key=request.values.get("key")
    refer=request.values.get("refer")
    if(key=="_id"):
        todos_l = todos.find({refer:ObjectId(key)})
    else:
        todos_l = todos.find({refer:key})
    return render_template('searchlist.html',todos=todos_l,t=title,h=heading)






if __name__ == "__main__":
    app.run()
