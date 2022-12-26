
from  mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re





EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile (r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')



class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']


    @staticmethod
    def validate(user):
        is_valid=True
        if len(user["first_name"])<2:
            flash("Nombre debe tener al menos 3 caracteres", 'register')
            is_valid=False
        
        if len(user["last_name"])<2:
            flash("Apellido debe tener al menos 3 caracteres", 'register')
            is_valid=False

        if not EMAIL_REGEX.match(user['email']): 
            flash("Direccion de correo electronico invalida", 'register')
            is_valid = False

        if not PASSWORD_REGEX.match(user["password"]):
            flash("La contraseña debe tener almenos 8 caracteres, mayusculas, minusculas y numeros", 'register')
            is_valid = False

        if user["password"]!= user["password_confirm"] :
            flash("Las contraseñas no coinciden", 'register')
            is_valid = False
        
        return is_valid




    @classmethod
    def check_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL('login').query_db(query,data)

        if len(results) <1:
            return False
        else:
            return cls(results[0])



    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name,last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now())"
        return connectToMySQL('login').query_db(query,data)



    @classmethod
    def get_with_credentials(cls, data):
        query = '''SELECT * FROM users where email=%(email)s'''

        results = connectToMySQL('login').query_db(query, data)

        return cls(results[0])










