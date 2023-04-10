import torch
import cv2
import numpy as np

#leemos el modelo
model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'C:/Users/migue/Desktop/yolo/yolo/YOLOv5/bestv5.pt' )

cap = cv2.VideoCapture('video1.mp4')

while True:
    success, frame = cap.read()

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
    t = cv2.waitKey(5)
    if t == ord('p'):
        print(f"se detectaron {num_persona} personas")

    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()