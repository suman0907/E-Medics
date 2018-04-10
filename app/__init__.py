from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from flask import Flask
import lib.log as log
import logging
from config import config, APP_NAME

Logger = logging.getLogger(APP_NAME)

db = SQLAlchemy()

def initialize_db(app):
    db.init_app(app)
    import models, medical_store.product.models_product, medical_store.order.models_order, \
        medical_store.registration_page.models_register
    migrate = Migrate(app, db)


def create_app(config_name):
    app = Flask(__name__)
    CORS(app,resources={r"":{"origins":""}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    log.setup_logging(config[config_name])

    initialize_db(app)



    from app.medical_store.product.views_product import products as suman
    app.register_blueprint(suman, url_prefix='/product')

    from app.medical_store.registration_page.views_register import user_register as suman
    app.register_blueprint(suman, url_prefix='/register')

    return app
