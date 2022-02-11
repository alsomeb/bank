from flask import Flask
from website.models import db, User, user_manager
from flask_mail import Mail


app = Flask(__name__) # Startar Flask APP
mail = Mail(app)
app.config.from_object('website.config.ConfigDebug')

db.app = app
db.init_app(app) #init db
user_manager.app = app
user_manager.init_app(app,db,User) #init user_manager
mail.init_app(app) # init mailservice

#Routes - BP
from .views import views
from .api import api
from .mailService import mailService

#Blueprints
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(api, url_prefix="/")
app.register_blueprint(mailService, url_prefix="/")