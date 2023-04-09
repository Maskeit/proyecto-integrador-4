import cv2
import argparse
import numpy as np
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
            break
    pass

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
