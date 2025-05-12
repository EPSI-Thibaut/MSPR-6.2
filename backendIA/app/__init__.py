from flask import Flask
from app.config import Config
from app.models import db
from app.routes import main
from flask_migrate import Migrate
from app.ia_model import CovidForecaster

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(main)

    return app