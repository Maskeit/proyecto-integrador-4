#Version de Yolo 8
# deteccion de personas exitoso pero consume muchos recursos el modelo
# upd, ya no consume muchos recursos, solo usando variables de tiempos
import cv2
import argparse
import time
from ultralytics import YOLO
import supervision as sv

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
    cursor.execute("INSERT INTO public.\"aforoReg_register\" (id_place, id_cam, personas) VALUES (%s, %s, %s)", (8, 4, num_persona))
    #(6, 2, num_persona) 6 = casa Miguel && 2 = camara desktop MIguel
    #(8, 4, num_persona) 8 = salon 4D && 4 = camara Laptop Miguel
    #(8, 5, num_persona) 8 = salon 4D && 5 = raspberry
    #(6, 6, num_persona) 6 = casa Miguel 4D && 6 = raspberry
    conn.commit()
    # Cerrar la conexión
    conn.close()
def parse_arguments() ->argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8live")
    parser.add_argument(
        "--webcam-resolution",
        default=[1280,720],
        nargs=2,
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    cap = cv2.VideoCapture(0)
    frame_width, frame_height = args.webcam_resolution

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("models/yolov8l.pt") #modelo prentrenado del repo de ultralytics

    box_annotator = sv.BoxAnnotator(thickness=2,text_thickness=2,text_scale=1)

    # Variables para el control del tiempo de detección
    last_detection_time = 0
    detection_interval = 4  # segundos

    while True:
        success, frame = cap.read()
        # Realizar detecciones si han pasado al menos detection_interval segundos desde la última detección
        current_time = time.time()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
        if success and current_time - last_detection_time >= detection_interval:

            result = model(frame)[0]
            detections = sv.Detections.from_yolov8(result)
            detections = detections[detections.class_id ==0] #para descartar los demas objetos hay que cambiar el valor de la class_id == 0
            labels =  [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, _ in detections
            ]
            frame = box_annotator.annotate(scene=frame,
                                           detections=detections,
                                           labels=labels
                                           ) #3 argumentos, scene, detections, labels
            # Display numero de personas detectadas
            num_persona = len(detections)
            last_detection_time = current_time
            cv2.imshow("yolov8", frame)
            print(num_persona)
            if num_persona != 0:
                enviarData(num_persona)
            else:
                print("No hay datos para enviar")
            if (cv2.waitKey(1) == 27):
                break
    pass

if __name__ == "__main__":
    main()
