from flask import Blueprint, request, jsonify
from ..db_2 import get_db_connection

cont_routes = Blueprint("cont_routes", __name__)

@cont_routes.route('/cont', methods=['POST'])
def upload_data():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos mal enviados"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    for nodo, values in data.items():
        for reg in values:
            print(nodo, reg['d01'], reg['d25'], reg['d10'])
            cursor.execute('''
                INSERT INTO T_Conta (nodo, d01, d25, d10)
                VALUES (?, ?, ?, ?)
            ''', (nodo, reg['d01'], reg['d25'], reg['d10'] ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Datos insertados correctamente"}), 200

@cont_routes.route('/cont', methods=['GET'])
def get_cont():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consulta a la bd
        cursor.execute('SELECT * FROM T_conta')
        rows = cursor.fetchall()
        
        conn.close()
        return jsonify({"data": rows}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500