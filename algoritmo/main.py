import torch
import cv2
import numpy as np
import time
#Bloque para la funcion de enviar el dato a otro archivo
import socket
import psycopg2

def enviarData(num_persona):
    # Conectar la base de datos
    conn = psycopg2.connect(
        host="smart-crowd.postgres.database.azure.com",
        database="smart-crowd",
        user="django@smart-crowd",
        password="MAdj2023!*",
        sslmode="require"
    )

    # Crear cursor
    cursor = conn.cursor()
    # Insertar los valores en la tabla
    #consulta = f"INSERT INTO nombre_tabla (columna_resultado) VALUES ({operacion})"
    cursor.execute("INSERT INTO public.\"aforoReg_register\" (id_place, id_cam, personas) VALUES (%s, %s, %s)", (8, 1, num_persona))
    conn.commit()
    # Cerrar la conexión
    conn.close()


    # # Crear socket y conectar con el servidor
    # HOST = 'localhost'  # Host del servidor
    # PORT = 18748  # Puerto utilizado por el servidor
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     # Enviar el número de personas detectadas como una cadena de texto
    #     s.sendall(str(num_persona).encode())
    #     # Esperar respuesta del servidor (opcional)
    #     data = s.recv(1024)
    #     print(f"Respuesta del servidor: {data.decode()}")
#

#leemos el modelo
model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'C:/Users/ximen/PycharmProjects/pythonProject/proyectoOpenCV/yolo/proyecto-integrador-4/algoritmo/bestv5.pt' )

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Aumentar el brillo multiplicando los valores de los pixeles
print('Dispositivo de ejecución:', torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

# Variables para el control del tiempo de detección
last_detection_time = 0
detection_interval = 4 # segundos

while True:
    success, frame = cap.read()
    # Realizar detecciones si han pasado al menos detection_interval segundos desde la última detección
    current_time = time.time()
    if success and current_time - last_detection_time >= detection_interval:
        brillo = 40
        frame = cv2.convertScaleAbs(frame, beta=brillo)
        detect = model(frame)
        num_persona = 0
        for det in detect.xyxy[0]:
            if det[5] == 0:
                num_persona +=1
        cv2.imshow('detector de personas', np.squeeze(detect.render()))
        last_detection_time = current_time # Actualizar el tiempo de la última detección
        print(f"Se detectaron {num_persona} personas")
        if num_persona:
            enviarData(num_persona)
        else:
            break
    # leer el teclado
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()