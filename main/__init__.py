from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Programma girin!'
login_manager.login_message_category = 'info'

from . import routes_library
from . import routes_lms, models, forms
from . import routes_hometasks