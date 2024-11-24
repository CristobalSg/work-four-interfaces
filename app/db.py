import sqlite3
from flask import current_app

# Función para obtener la conexión a la base de datos
def get_db_connection():
    # conn = sqlite3.connect(current_app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", ""))
    # conn.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre
    conex = sqlite3.connect('Imagenes.db')
    # conn = conex.cursor()
    return conex

# Función para crear la tabla si no existe
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS T_Img (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imagen_original BLOB,
            canal_R BLOB,
            canal_G BLOB,
            canal_B BLOB,
            imagen_gris BLOB
        )
    ''')
    conn.commit()
    conn.close()
