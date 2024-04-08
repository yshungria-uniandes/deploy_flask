from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

DB_NAME = 'recipes_schema'

FIRST_LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]{2}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]{8}')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query = '''
                INSERT INTO users (first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                '''
        response_query_users = connectToMySQL(DB_NAME).query_db(query,data)
        return response_query_users

    @classmethod
    def get_user_by_email(cls,data):
        query = '''
                SELECT * FROM users WHERE email = %(email)s
                '''
        response_user=connectToMySQL(DB_NAME).query_db(query,data)
        if len(response_user)<1:
            return False
        return cls(*response_user)
    
    @classmethod
    def get_user_by_id(cls,data):
        query = '''
                SELECT * FROM users WHERE id = %(id)s
                '''
        response_user=connectToMySQL(DB_NAME).query_db(query,data)
        return cls(*response_user)

    @staticmethod
    def validate_registration(registro):      
        query = '''
                SELECT * FROM users WHERE email=%(email)s
                '''
        response_query_user=connectToMySQL(DB_NAME).query_db(query,registro)
     
        is_valid = True
        print(registro)
        if not FIRST_LAST_NAME_REGEX.match(registro['firstname']):
            flash('al menos 2 letras para el nombre','register') 
            is_valid = False
        if not FIRST_LAST_NAME_REGEX.match(registro['lastname']):
            flash('al menos 2 letras para el apellido','register') 
            is_valid = False
        if not EMAIL_REGEX.match(registro['email']):
            flash("el correo no esta en el formato adecaudo",'register')
            is_valid=False
        if not registro['password1']==registro['password2']:
            flash('las contraseñas no coinciden','register')
            is_valid=False
        if not PASSWORD_REGREX.match(registro['password1']):
            flash("el password debe contener al menos 8 caracteres",'register')
            is_valid= False 
        if len(response_query_user)>=1:
            flash("el correo ya existe",'register')
            is_valid= False 
        return is_valid
    
    @staticmethod
    def validate_login(login):
        is_valid=True
        query = '''
                SELECT * FROM users WHERE email=%(email)s
                '''
        response_query_user=connectToMySQL(DB_NAME).query_db(query,login)
        
        if not len(response_query_user)>=1:
            flash("El correo no existe","login")
            is_valid=False
            return {'user':response_query_user,'is_valid':is_valid}
        
        return {'user':response_query_user[0],'is_valid':is_valid}