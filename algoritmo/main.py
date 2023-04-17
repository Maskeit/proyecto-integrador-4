import torch
import cv2
import numpy as np
import time
#Bloque para la funcion de enviar el dato a otro archivo
import socket

def enviarData(num_persona):
    # Crear socket y conectar con el servidor
    HOST = 'localhost'  # Host del servidor
    PORT = 12345  # Puerto utilizado por el servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Enviar el número de personas detectadas como una cadena de texto
        s.sendall(str(num_persona).encode())
        # Esperar respuesta del servidor (opcional)
        data = s.recv(1024)
        print(f"Respuesta del servidor: {data.decode()}")
#

#leemos el modelo
model = torch.hub.load('ultralytics/yolov5', 'custom', path ='models/bestv5.pt')

cap = cv2.VideoCapture(2)
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