from .db import create_table
from .db_2 import create_table_2
from flask import Flask
from .config import Config
from .routes.cont_routes import cont_routes
from .routes.image_routes import image_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Crear la base de datos y la tabla si no existe
    create_table()
    create_table_2()

    # Registrar las rutas
    app.register_blueprint(image_routes)
    app.register_blueprint(cont_routes)

    return app
