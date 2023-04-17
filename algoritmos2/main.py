import torch
import cv2
import numpy as np
import time
#Bloque para la funcion de enviar el dato a otro archivo
import socket

def enviarData(num_persona):
    HOST = 'localhost'
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            num_persona = int(num_persona)
            s.sendall(str(num_persona).encode())
            data = s.recv(1024)
            print(f"Respuesta del servidor: {data.decode()}")
        except (socket.timeout, ConnectionRefusedError, ValueError):
            print('No se pudo conectar con el servidor')
        finally:
            s.close()
    time.sleep(1) #Esperar un segundo antes de intentar conectarse
#
###############################################################################################
#leemos el modelo
model = torch.hub.load('ultralytics/yolov5', 'custom', path ='../algoritmo/models/bestv5.pt') #bestv5.pt #yolov5s.pt

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Aumentar el brillo multiplicando los valores de los pixeles
#print('Dispositivo de ejecución:', torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

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
                num_persona += 1
        cv2.imshow('detector de personas', np.squeeze(detect.render()))
        last_detection_time = current_time  # Actualizar el tiempo de la última detección
        print(f"Se detectaron {num_persona} personas")
        if num_persona:
            enviarData(num_persona)
        time.sleep(1)
    cv2.waitKey(1)
    if cv2.getWindowProperty('Detector de personas', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()