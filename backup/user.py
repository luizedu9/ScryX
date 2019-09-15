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
from werkzeug.security import check_password_hash

class User(object):
    def __init__(self, username, password, name, email, birthdate, gender, entrydate=date.today(), admin=False):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__email = email
        self.__birthdate = birthdate
        self.__gender = gender
        self.__entrydate = entrydate
        self.__admin = admin

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
    def admin(self):
        return self.__admin

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # REQUERIDO PELO FLASK_LOGIN
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.username)