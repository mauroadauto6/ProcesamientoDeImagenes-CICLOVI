import cv2
import pickle
import numpy as np

asientos = []
with open('cafeteria-pkl/cafeteria.pkl', 'rb') as file:
    asientos = pickle.load(file)

video = cv2.VideoCapture('cafeteria-deteccion/video-cafeteria-estabilizado.mp4')

while True:
    check, img = video.read()
    imgBGR2GRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBGRTH = cv2.adaptiveThreshold(imgBGR2GRAY, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgBGRMedian = cv2.medianBlur(imgBGRTH, 5)
    kernelBGR = np.ones((5,5), np.int8)
    imgBGRDil = cv2.dilate(imgBGRMedian, kernelBGR) 

    for x, y, w, h in asientos:
        espacio = imgBGRDil[y:y+h, x:x+w]
        count = cv2.countNonZero(espacio)
        
        if count < 1600:
            cv2.putText(img, str(count), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.putText(img, str(count), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('video', img)
    #cv2.imshow('BGR TO GRAY', imgBGR2GRAY)
    #cv2.imshow('BGR-GRAY TH', imgBGRTH)
    #cv2.imshow('video BGR Median', imgBGRMedian)
    #cv2.imshow('video BGR Dilatada', imgBGRDil)
    
    key = cv2.waitKey(10)
    if key == 32:  
        break