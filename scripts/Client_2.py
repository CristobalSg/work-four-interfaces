import numpy as np
import requests, time, io, os
from random import randint
import matplotlib.pyplot as plt
from telegram import Bot
from telegram import InputFile
from dotenv import load_dotenv

BASE_URL = "http://127.0.0.1:5000"

def post_data():
    dMP = {
        'N1' : [
            {
                'd01': randint(1, 10),
                'd25': randint(1, 10),
                'd10': randint(1, 10)
            }
        ],
        'N2' : [
            {
                'd01': randint(1, 10),
                'd25': randint(1, 10),
                'd10': randint(1, 10)
            }
        ],
        'N3' : [
            {
                'd01': randint(1, 10),
                'd25': randint(1, 10),
                'd10': randint(1, 10)
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/cont", json=dMP)
    if response.status_code == 200:
        print("Dato evniado correctamente:", response.json())
    else:
        print("Error al enviar el dato:", response.text)

def get_data(nodo):
    # Datos
    response = requests.get(f"{BASE_URL}/cont")
    d01 = []; d25 = []; d10 = []

    for i in range(100):
        if response.json()['data'][i][1] == nodo:
            d01.append(response.json()['data'][i][2])
            d25.append(response.json()['data'][i][3])
            d10.append(response.json()['data'][i][4])
    
    #  ________ Gráfico ________
    fig, ax = plt.subplots(figsize=(14,4))

    #_/ Datos
    x1 = np.arange(1, len(d01) + 1)
    x2 = np.arange(1, len(d25) + 1)
    x3 = np.arange(1, len(d10) + 1)

    ax.plot(x1, d01, color="k", marker = "s", markerfacecolor = 'red', label="d01") 
    ax.plot(x2, d25, color="k", marker = "s", markerfacecolor = 'green', label="d25") 
    ax.plot(x3, d10, color="k", marker = "s", markerfacecolor = 'blue', label="d10") 

    #_/ Diseño gráfico
    plt.title(f"Grafica de {nodo}")
    plt.xlabel('Cantidad de datos')
    plt.ylabel('Contaminación')
    plt.grid(True)
    ax.legend()
    
    # Guardar el gráfico en un archivo en memoria
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)  # Rewind the stream to the beginning
    
    # Enviar el gráfico a través de Telegram
    bot = Bot(token=token)
    bot.send_photo(chat_id=chat_id, photo=InputFile(img_stream, filename="grafico.png"))

    plt.show()

    if response.status_code == 200:
        print("Dato recibidos correctamente:")
    else:
        print("Error al recibir el dato:", response.text)

if __name__ == "__main__":
    interruptors = [0, 1]

    # PARTE 2 ENVIAR CONTAMINACIÓN
    if interruptors[0] == 1:
        for i in range(50):
            post_data()
            # time.sleep(3)
    
    # Llamada a la función (ejemplo)
    nodo = "N1"
    token = os.getenv('TELEGRAM_TOKEN')  # Sustituir por tu token del bot de Telegram
    chat_id = "falta el id"  # Sustituir por tu chat ID de Telegram
    # PARTE 3 ENVIAR TELEGRAM
    if interruptors[1] == 1:
        get_data('N1', token, chat_id)