# -*- coding: utf-8 -*-


#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE AUXÍLIO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira
#
#   user.py:
#   Este modulo define a classe usuario

from datetime import date

class User(object):
    def __init__(self, username, password, name, email, birthdate, gender):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__email = email
        self.__birthdate = birthdate
        self.__gender = gender
        self.__entrydate = date.today()
        self.__budget = []

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def birthdate(self):
        return self.__birthdate

    @property
    def gender(self):
        return self.__gender

    @property
    def entrydate(self):
        return self.__entrydate

    @property
    def budget(self):
        return self.__budget

    @budget.setter
    def budget(self, value):
        self.__budget.append(value)