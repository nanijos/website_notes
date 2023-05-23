from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from pymongo import MongoClient


db = SQLAlchemy()
DB_NAME = "database.db"

connection_string='mongodb+srv://josbu:Newyorkcity@josr.c1v4iey.mongodb.net/Data'
client = MongoClient(connection_string)
#dbs = client.list_database_names()

# Replace "mydatabase" with your desired database name
db = client["mydatabase"]


web_db=client.web
# collections=web_db.list_collections_names()
#print(collections)

collection = db["mycollection"]
documents = collection.find()
for document in documents:
    print(document)




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'




    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
