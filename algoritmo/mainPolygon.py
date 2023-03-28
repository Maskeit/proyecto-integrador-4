import cv2
import argparse

import numpy as np
from ultralytics import YOLO
import supervision as sv

ZONE_POLYGON = np.array([
    [0,0],
    [1280 // 2,0],
    [1250 // 2, 720],
    [0,720]
])
def parse_arguments() ->argparse.Namespace:
    parser = argparse.ArgumentParser(description="YYOLOv8live")
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
    cap = cv2.VideoCapture(1)

    frame_width, frame_height = args.webcam_resolution

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(thickness=2,text_thickness=2,text_scale=1)

    zone = sv.PolygonZone(polygon=ZONE_POLYGON, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone,
                                             color=sv.Color.red(),
                                             thickness=2,
                                             text_thickness=4,
                                             text_scale=2)


    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame,1)

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        detections = detections[detections.class_id ==0] #para descartar los demas objetos hay que cambiar el valor de la class_id == 0

        labels =  [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _ in detections
        ]
        frame = box_annotator.annotate(scene=frame,
                                       detections=detections,
                                       labels=labels
                                       )
        # zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)

        cv2.imshow("yolov8", frame)
        if(cv2.waitKey(1) == 27):
            break
    pass

if __name__ == "__main__":
    main()