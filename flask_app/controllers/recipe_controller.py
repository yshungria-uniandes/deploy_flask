from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models.recipe_model import Recipe
from datetime import datetime

@app.route("/recipes/new",methods=['GET',"POST"])
def create_recipe():
    if request.method=='GET':    
        if 'id' not in session:
            return redirect('/logout')
        return render_template("create_recipe.html")
    elif request.method=='POST':
        if not Recipe.validate_recipe_form(request.form):
            return redirect("/recipes/new")
        data = {
            'name':request.form['name'],
            'description':request.form['description'],
            'instruction':request.form['instruction'],
            'created_at':request.form['date'],
            'under_30_minutes':int(request.form['minutes']),
            'user_id':session['id']
        }    
        creating_recipe=Recipe.create_new_recipe(data)
        print("new recipe created", creating_recipe)
        return redirect("/dashboard")
   
@app.route("/recipes/<int:id>",methods=['GET'])
def read_recipe(id):
    
    data_id={
        "id":session['id']
    }
    if not Recipe.validate_user_recipe(data_id,id):
        return redirect("/danger")
    
    data = {
        'id':id
    }
    resultado = Recipe.get_recipe_by_id(data)
    resultado.created_at = resultado.created_at.strftime("%d %B, %Y")
    return render_template("read_recipe.html",recipe=resultado)
@app.route("/recipes/edit/<int:id>",methods=['GET','POST'])
def edit_recipe(id):
    if request.method == 'GET':

        data_id={
        "id":session['id']
        }
        if not Recipe.validate_user_recipe(data_id,id):
            return redirect("/danger")

        data = {
            'id':id
        }
        resultado = Recipe.get_recipe_by_id(data)
        resultado.created_at = resultado.created_at.strftime("%Y-%m-%d")
        return render_template("edit_recipe.html",recipe=resultado)
    if request.method == 'POST':
        if not Recipe.validate_recipe_form(request.form):
            return redirect(f"/recipes/edit/{id}")
        data = {
            'name':request.form['name'],
            'description':request.form['description'],
            'instruction':request.form['instruction'],
            'created_at':request.form['date'],
            'under_30_minutes':int(request.form['minutes']),
            'id':id
        }
        resultado = Recipe.update_recipe_by_id(data)
        print(resultado)
        return redirect("/dashboard")

@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    if 'id' not in session:
        return redirect('/logout')
    data_id={
        "id":session['id']
    }
    if not Recipe.validate_user_recipe(data_id,id):
        return redirect("/danger")
    data = {
        'id':id
    }
    print("aqui id para eliminar",id)
    print(Recipe.delete_recipe_by_id(data))    
    return redirect("/dashboard")

@app.route("/danger",methods=['GET'])
def danger_message():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip=request.environ['REMOTE_ADDR']
    else:
        ip= request.environ['HTTP_X_FORWARDED_FOR'] 
    return render_template("danger.html",ip=ip)