import torch
import cv2
import numpy as np
<<<<<<< HEAD
from ultralytics import YOLO
import supervision as sv

import socket

##aqui se detiene un poco
ZONE_POLYGON = np.array([
    [0,0],
    [800,0], #left side
    [800 , 608],
    [0,608]#right side
])
def parse_arguments() ->argparse.Namespace:
    parser = argparse.ArgumentParser(description="YYOLOv8live")
    parser.add_argument(
        "--webcam-resolution",
        default=[640,352], #1280, 720
        nargs=2,
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    cap = cv2.VideoCapture('video.mp4') #web cam en (720, 1280, 3) y #img en (352, 640, 3)

    frame_width, frame_height = args.webcam_resolution

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("best.pt") #yolov8l modelo prentrenado por miguel

    box_annotator = sv.BoxAnnotator(thickness=2,text_thickness=2,text_scale=1)
    #
    zone = sv.PolygonZone(polygon=ZONE_POLYGON,frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone,
                                             color=sv.Color.white(),
                                             thickness=2,
                                             text_thickness=4,
                                             text_scale=2
                                            )

    while True:
        success, frame = cap.read()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

        result = model(frame)[0]
        detections = sv.Detections.from_yolov8(result)
        detections = detections[detections.class_id == 0] #para descartar los demas objetos hay que cambiar el valor de la class_id == 0


        labels =  [
            f"{model.model.names[class_id]} {confidence:0.5f}"
            for _, confidence, class_id, _ in detections
        ]
        frame = box_annotator.annotate(scene=frame,
                                       detections=detections,
                                       labels=labels
                                       )
        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)
        if cv2.waitKey(1) == ord('p'):
            num_personas = len(detections)
            print(f"Se detectaron {num_personas} personas")



        cv2.imshow("yolov8", frame)
        # print(frame.shape)
        # break
        if(cv2.waitKey(1) == 27):
=======
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
>>>>>>> main
            break
    # leer el teclado
    cv2.waitKey(1)

<<<<<<< HEAD
if __name__ == "__main__":
    main()
#creamos el objeto de conexion para el servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5000))
s.listen(5)
# creamos el objeto de conexion para el servidor
clienSocket, address = s.accept()
print(f"La conexion desde {address} ha sido establecida!")
clienSocket.send(bytes(len(detections)))
=======
cap.release()
cv2.destroyAllWindows()
>>>>>>> main
