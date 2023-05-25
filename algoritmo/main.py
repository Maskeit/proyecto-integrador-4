import torch
import cv2
import numpy as np
import time
#Bloque para la funcion de enviar el dato a otro archivo
import psycopg2

def enviarData(num_persona):
    # Conectar la base de datos
    conn = psycopg2.connect(
        host="smartcrowd.postgres.database.azure.com",
        database="smartcrowd",
        user="django@smartcrowd",
        password="MAdj2023!*",
        sslmode="require"
    )

    # Crear cursor
    cursor = conn.cursor()
    # Insertar los valores en la tabla
    #consulta = f"INSERT INTO nombre_tabla (columna_resultado) VALUES ({operacion})"
    cursor.execute("INSERT INTO public.\"aforoReg_register\" (id_place, id_cam, personas) VALUES (%s, %s, %s)", (4, 3, num_persona))
    # Salon: 2,1
    # Cafeteria: 3,2
    # Casa Miguel: 4,3
    conn.commit()
    # Cerrar la conexión
    conn.close()
#

#leemos el modelo
model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'C:/Users/migue/Desktop/yolo/yolo/YoloV5/bestv5.pt' )

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Variables para el control del tiempo de detección
last_detection_time = 0
detection_interval = 2 # segundos

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
        if num_persona != 0:
            enviarData(num_persona)
        else:
            print("No hay datos que enviar.")
        print("Esperando próxima detección...")
    # leer el teclado
    t = cv2.waitKey(1)
    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()
