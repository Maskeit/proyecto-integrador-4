import cv2
import numpy

filename= 'img3.jpg'
#comentario de prueba

def detect(filename):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()

    #img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print('Caras detectadas: ', len(faces))

        for(x,y,w,h) in faces:
            img = cv2.rectangle(img, (x,y), (x+w,y+h),(255,0,0),2)
        cv2.namedWindow('WhiteChican detected!!')
        cv2.imshow('Whitechikan',img)
        #cv2.imwrite('newImg.jpg',img)

        k = cv2.waitKey(30)
        if k == 27:
            break

detect(filename)