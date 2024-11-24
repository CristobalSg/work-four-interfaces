from PIL import Image
import io, os, time, base64, requests

# URL base del backend Flask
BASE_URL = "http://127.0.0.1:5000"

def process_image(file_path):
    """
    Lee la imagen, separa los canales R, G, B y convierte a escala de grises.
    Retorna un diccionario con los datos procesados.
    """
    try:
        # Abrir la imagen
        with Image.open(file_path) as img:
            img = img.convert("RGB")  # Asegurarse de que esté en formato RGB
            
            # Separar los canales
            r, g, b = img.split()
            
            # Convertir a escala de grises
            grayscale = img.convert("L")
            
            # Convertir los canales a bytes
            r_bytes = io.BytesIO()
            g_bytes = io.BytesIO()
            b_bytes = io.BytesIO()
            grayscale_bytes = io.BytesIO()
            original_bytes = io.BytesIO()
            
            r.save(r_bytes, format="JPEG")
            g.save(g_bytes, format="JPEG")
            b.save(b_bytes, format="JPEG")
            grayscale.save(grayscale_bytes, format="JPEG")
            img.save(original_bytes, format="JPEG")
            
            return {
                "imagen_original": original_bytes.getvalue(),
                "canal_R": r_bytes.getvalue(),
                "canal_G": g_bytes.getvalue(),
                "canal_B": b_bytes.getvalue(),
                "imagen_gris": grayscale_bytes.getvalue(),
            }
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None

def post_image(file_path):
    """
    Procesa la imagen y envía los datos al backend Flask.
    """
    image_data = process_image(file_path)
    if not image_data:
        print("No se pudo procesar la imagen.")
        return
    
    try:
        # Crear la carga útil para enviar los archivos
        files = {
            "imagen_original": ("original.jpg", image_data["imagen_original"], "image/jpeg"),
            "canal_R": ("r_channel.jpg", image_data["canal_R"], "image/jpeg"),
            "canal_G": ("g_channel.jpg", image_data["canal_G"], "image/jpeg"),
            "canal_B": ("b_channel.jpg", image_data["canal_B"], "image/jpeg"),
            "imagen_gris": ("grayscale.jpg", image_data["imagen_gris"], "image/jpeg"),
        }   
        
        # Hacer la solicitud POST
        response = requests.post(f"{BASE_URL}/img", files=files)
        if response.status_code == 200:
            print("Imagen enviada correctamente:", response.json())
        else:
            print("Error al enviar la imagen:", response.text)
    except Exception as e:
        print(f"Error al enviar la imagen: {e}")

def display_images(images):
    """
    Muestra las imágenes procesadas en una interfaz gráfica utilizando Tkinter.
    """
    import tkinter as tk
    from tkinter import Label
    from PIL import ImageTk

    # Crear la ventana de Tkinter
    root = tk.Tk()
    root.title("Imágenes Procesadas")

    # Crear un título para cada imagen y mostrarlas
    labels = [
        ("Imagen Original", images["imagen_original"]),
        ("Canal R", images["canal_R"]),
        ("Canal G", images["canal_G"]),
        ("Canal B", images["canal_B"]),
        ("Escala de Grises", images["imagen_gris"])
    ]

    # Colocar cada imagen y su título en la ventana
    for idx, (title, img) in enumerate(labels):
        img_tk = ImageTk.PhotoImage(img)
        label_title = Label(root, text=title)
        label_title.grid(row=idx*2, column=0, padx=10, pady=5)
        label_img = Label(root, image=img_tk)
        label_img.image = img_tk  # Necesario para evitar que la imagen se elimine de la memoria
        label_img.grid(row=idx*2+1, column=0, padx=10, pady=5)

    # Iniciar el bucle de la interfaz gráfica
    root.mainloop()

def fetch_images():
    response = requests.get("http://127.0.0.1:5000/img")

    if response.status_code == 200:
        data = response.json()
        images = data.get("images", [])

        for img in images:
            print(f"ID: {img['id']}")
            # delete_image(img['id']) # eliminar imagenes all

            if img['id'] == 97:
                # Decodificar las imágenes en base64
                original = Image.open(io.BytesIO(base64.b64decode(img["imagen_original"])))
                canal_R = Image.open(io.BytesIO(base64.b64decode(img["canal_R"])))
                canal_G = Image.open(io.BytesIO(base64.b64decode(img["canal_G"])))
                canal_B = Image.open(io.BytesIO(base64.b64decode(img["canal_B"])))
                imagen_gris = Image.open(io.BytesIO(base64.b64decode(img["imagen_gris"])))

                # Llamar a la función display_images y mostrar las imágenes
                images_data = {
                    "imagen_original": original,
                    "canal_R": canal_R,
                    "canal_G": canal_G,
                    "canal_B": canal_B,
                    "imagen_gris": imagen_gris
                }

                # Mostrar las imágenes en la interfaz gráfica
                display_images(images_data)
    else:
        print("Error al obtener imágenes:", response.text)

def delete_image(image_id):
    """
    Envía una solicitud DELETE para eliminar una imagen por ID.
    """
    try:
        response = requests.delete(f"{BASE_URL}/img/{image_id}")
        if response.status_code == 200:
            print(f"Imagen con ID {image_id} eliminada correctamente.")
        elif response.status_code == 404:
            print(f"No se encontró una imagen con ID {image_id}.")
        else:
            print(f"Error al eliminar imagen: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    folder_path = "./IMG"  # Carpeta donde están las imágenes

    # Comprobar si la carpeta existe
    # if not os.path.exists(folder_path):
    #     print(f"La carpeta {folder_path} no existe.")
    # else:
    #     # Recorrer todos los archivos de la carpeta
    #     for file_name in os.listdir(folder_path):
    #         file_path = os.path.join(folder_path, file_name)
            
    #         # Verificar si el archivo es una imagen (opcional)
    #         if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
    #             print(f"Procesando: {file_path}")
    #             post_image(file_path)

    #             # Esperar 3 segundos antes de procesar la siguiente imagen
    #             time.sleep(3)
    #         else:
    #             print(f"Saltando archivo no compatible: {file_name}")

    # Consultar las imágenes almacenadas después de procesarlas
    # fetch_images()