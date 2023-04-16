import torch
import cv2
import numpy as np

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
model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'C:/Users/migue/Desktop/yolo/yolo/YoloV5/bestv5.pt' )

cap = cv2.VideoCapture('video1.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Aumentar el brillo multiplicando los valores de los pixeles
print('Dispositivo de ejecución:', torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

while True:
    success, frame = cap.read()
    brillo = 70
    frame = cv2.convertScaleAbs(frame, beta=brillo)
    # Realizar detecciones
    detect = model(frame)
    #contar el numero de personas detectadas
    num_persona = 0
    for det in detect.xyxy[0]:
        if det[5] == 0:
            num_persona +=1

    #mostramos fps
    cv2.imshow('detector de personas', np.squeeze(detect.render()))
    # print(frame.shape) (480, 640, 3)
    # leer el teclado
    t = cv2.waitKey(5000)
    if t != ord('p'):
        print(f"se detectaron {num_persona} personas")
        enviarData(num_persona)

    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()