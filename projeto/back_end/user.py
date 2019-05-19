# -*- coding: utf-8 -*-


#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE AUXÍLIO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira
#
#   user.py:
#   Este modulo define a classe usuario

class User(object):
    def __init__(self, id, username, password, name, email, birthdate, gender, entrydate, budgetCounter, budget):
        self._id = id
        self._username = username
        self._password = password
        self._name = name
        self._email = email
        self._birthdate = birthdate
        self._gender = gender
        self._entrydate = entrydate
        self._budgetCounter = 0
        self._budget = [] # ************************************************************************************

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def birthdate(self):
        return self._birthdate

    @property
    def gender(self):
        return self._gender

    @property
    def entrydate(self):
        return self._entrydate

    @property
    def budgetCounter(self):
        return self._budgetCounter

    @budgetCounter.setter
    def budgetCounter(self, value):
        self._budgetCounter = value

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        self._budget.append(value)