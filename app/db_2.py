import sqlite3

def get_db_connection():
    conex = sqlite3.connect('Contaminación.db')
    return conex

def create_table_2():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''                 
        CREATE TABLE IF NOT EXISTS T_Conta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nodo VARCHAR(2) NOT NULL,
            d01 INTEGER NOT NULL,
            d25 INTEGER NOT NULL,
            d10 INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
