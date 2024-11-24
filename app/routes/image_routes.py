from flask import Blueprint, request, jsonify
from ..db import get_db_connection
import base64

image_routes = Blueprint("image_routes", __name__)

@image_routes.route('/img', methods=['GET'])
def get_images():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consulta a la bd
        cursor.execute('SELECT id, imagen_original, canal_R, canal_G, canal_B, imagen_gris FROM T_Img')
        rows = cursor.fetchall()
        
        images = []
        for row in rows:
            images.append({
                "id": row[0],
                "imagen_original": base64.b64encode(row[1]).decode("utf-8"),
                "canal_R": base64.b64encode(row[2]).decode("utf-8"),
                "canal_G": base64.b64encode(row[3]).decode("utf-8"),
                "canal_B": base64.b64encode(row[4]).decode("utf-8"),
                "imagen_gris": base64.b64encode(row[5]).decode("utf-8"),
            })
        conn.close()
        return jsonify({"images": images}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@image_routes.route('/img', methods=['POST'])
def upload_image():
    try:
        # Obtener los datos de la imagen desde la solicitud (en formato multipart)
        imagen_original = request.files['imagen_original'].read()
        canal_R = request.files['canal_R'].read()
        canal_G = request.files['canal_G'].read()
        canal_B = request.files['canal_B'].read()
        imagen_gris = request.files['imagen_gris'].read()

        if not imagen_original or not canal_R or not canal_G or not canal_B or not imagen_gris:
            return jsonify({"error": "Todos los archivos son requeridos"}), 400

        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar las imágenes en la base de datos
        cursor.execute('''
            INSERT INTO T_Img (imagen_original, canal_R, canal_G, canal_B, imagen_gris)
            VALUES (?, ?, ?, ?, ?)
        ''', (imagen_original, canal_R, canal_G, canal_B, imagen_gris))

        conn.commit()
        conn.close()
        print("---")
        return jsonify({"message": "Imagenes subidas correctamente!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@image_routes.route('/img/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """
    Elimina una imagen de la base de datos basada en su ID.
    """
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el registro existe
        cursor.execute("SELECT * FROM T_Img WHERE id = ?", (image_id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({"error": f"No se encontró una imagen con ID {image_id}"}), 404

        # Eliminar el registro
        cursor.execute("DELETE FROM T_Img WHERE id = ?", (image_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": f"Imagen con ID {image_id} eliminada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
