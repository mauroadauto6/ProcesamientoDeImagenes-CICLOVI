import cv2
import pickle
import numpy as np

asientos = []
with open('cafeteria-pkl/cafeteria.pkl', 'rb') as file:
    asientos = pickle.load(file)

video = cv2.VideoCapture('cafeteria-deteccion/video-cafeteria-estabilizado.mp4')

while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB2GRAY = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2GRAY)
    imgRGBTH = cv2.adaptiveThreshold(imgRGB2GRAY, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgRGBMedian = cv2.medianBlur(imgRGBTH, 5)
    kernelRGB = np.ones((5,5), np.int8)
    imgRGBDil = cv2.dilate(imgRGBMedian, kernelRGB)

    for x, y, w, h in asientos:
        espacio = imgRGBDil[y:y+h, x:x+w]
        count_white = cv2.countNonZero(espacio)
        count_black = (w*h) - count_white
        
        cv2.putText(img, ('White: ' + str(count_white)), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, ('Black: ' + str(count_black)), (x, y + h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        if ((count_black - count_white) % 2 == 1):
            cv2.putText(img, 'OCUPADO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            cv2.putText(img, 'VACIO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


    cv2.imshow('video', img)
    #cv2.imshow('RGB TO GRAY', imgRGB2GRAY)
    #cv2.imshow('RGB-GRAY TH', imgRGBTH)
    #cv2.imshow('video RGB Median', imgRGBMedian)
    #cv2.imshow('video RGB Dilatada', imgRGBDil)
    
    key = cv2.waitKey(10)
    if key == 32:  
        break