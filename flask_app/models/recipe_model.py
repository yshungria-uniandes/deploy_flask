from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
DB_NAME = 'recipes_schema'

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create_new_recipe(cls,data):
        query = '''
                INSERT INTO recipes (name,description,instruction,under_30_minutes,created_at,user_id)
                VALUES (%(name)s,%(description)s,%(instruction)s,%(under_30_minutes)s,%(created_at)s,%(user_id)s);
                '''
        response_query=connectToMySQL(DB_NAME).query_db(query,data)
        return response_query
    
    @classmethod
    def get_all_recipes(cls):
        query = '''
                SELECT * FROM recipes
                '''
        response_query_recipes=connectToMySQL(DB_NAME).query_db(query)
        recipes = []
        for recipe in response_query_recipes:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_all_recipes_by_id(cls,data):
        query = '''
                SELECT recipes.id,recipes.name,recipes.description,recipes.instruction,recipes.under_30_minutes,recipes.created_at,recipes.updated_at,recipes.user_id FROM users
                LEFT JOIN recipes ON users.id = recipes.user_id
                WHERE users.id = %(id)s;
                '''
        response_query_recipes=connectToMySQL(DB_NAME).query_db(query,data)
        if response_query_recipes[0]['id']== None:
            print([cls(response_query_recipes[0])])
            return [cls(response_query_recipes[0])]

        recipes=[]
        for recipe in response_query_recipes:
            recipe['under_30_minutes']=int.from_bytes((recipe['under_30_minutes']), "big")
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_recipe_by_id(cls,data):
        query = '''
                SELECT * FROM recipes WHERE id = %(id)s;
                '''
        response_query_recipes=connectToMySQL(DB_NAME).query_db(query,data)

        response_query_recipes[0]['under_30_minutes']=int.from_bytes((response_query_recipes[0]['under_30_minutes']), "big")
        # response_query_recipes[0]['created_at'] = response_query_recipes[0]['created_at'].strftime("%d %B, %Y")
        print(type(response_query_recipes[0]['created_at']))
        return cls(*response_query_recipes)
    
    @classmethod
    def update_recipe_by_id(cls,data):
        query = '''
                UPDATE recipes
                SET name=%(name)s,description=%(description)s,instruction=%(instruction)s,under_30_minutes=%(under_30_minutes)s,created_at=%(created_at)s,updated_at=NOW()
                WHERE id=%(id)s;
                '''
        response_query_update=connectToMySQL(DB_NAME).query_db(query,data)

        return response_query_update
    @classmethod
    def delete_recipe_by_id(cls,data):
        query = '''
                DELETE FROM recipes WHERE id=%(id)s;
                '''
        response_query_update=connectToMySQL(DB_NAME).query_db(query,data)

        return response_query_update

    @staticmethod
    def validate_recipe_form(data):
        is_valid=True

        if len(data['name'])<3:
            flash("El nombre necesita al menos 3 caracteres","create")
            is_valid=False
        if len(data['description'])<3:
            flash("La description necesita al menos 3 caracteres","create")
            is_valid=False
        if len(data['instruction'])<3:
            flash("Las instrucciones necesitan al menos 3 caracteres","create")
            is_valid=False
        if len(data['date'])==0:
            flash("Necesita agregar una fecha","create")
            is_valid=False
        
        return is_valid

    @staticmethod
    def validate_user_recipe(data,id):
        is_valid=True
        all_recipes=Recipe.get_all_recipes_by_id(data)
        count=0
        for recipe in all_recipes:
            if recipe.id==id:
                count += 1
        if count != 1:
              is_valid = False
        return is_valid