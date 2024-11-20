from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
# print(bcrypt.generate_password_hash(password='squid').decode('utf-8'))

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data.db'
    app.secret_key = 'KOLEJOHN'
    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # login settings
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page'
    login_manager.login_message_category = 'info'

    # user loader function

    from models import Employee

    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))

    #imports later on

    from routes import register_routes
    register_routes(app, db)

    migrate.init_app(app, db)

    return app