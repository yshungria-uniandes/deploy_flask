from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key= "keep it secret, keep it safe"

bcrypt = Bcrypt( app )