import os

class Config:
    # Definir la ruta de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = "sqlite:///Imagenes.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
