import cv2
import pickle
import numpy as np

asientos = []
with open('biblioteca-pkl/biblioteca.pkl', 'rb') as file:
    asientos = pickle.load(file)

video = cv2.VideoCapture('biblioteca-deteccion/biblioteca.mp4')

while True:
    check, img = video.read()
    imgBGR2GRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBGRTH = cv2.adaptiveThreshold(imgBGR2GRAY, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgBGRMedian = cv2.medianBlur(imgBGRTH, 5)
    kernelBGR = np.ones((5,5), np.int8)
    imgBGRDil = cv2.dilate(imgBGRMedian, kernelBGR) 

    for x, y, w, h in asientos:
        espacio = imgBGRDil[y:y+h, x:x+w]
        count_white = cv2.countNonZero(espacio)
        count_black = (w*h) - count_white
        total_rect = w * h
        
        cv2.putText(img, ('White: ' + str(count_white)), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, ('Black: ' + str(count_black)), (x, y + h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(img, ('Total: ' + str(total_rect)), (x, y + h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        """if (count_white < count_black / 3):
            cv2.putText(img, 'OCUPADO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            cv2.putText(img, 'VACIO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)"""
        
        if total_rect == 28684 or total_rect == 22692:
            if count_white < 9850 or count_white > 10500:
                cv2.putText(img, 'OCUPADO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            else:
                cv2.putText(img, 'VACIO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('video', img)
    #cv2.imshow('RGB TO GRAY', imgBGR2GRAY)
    #cv2.imshow('RGB-GRAY TH', imgBGRTH)
    #cv2.imshow('video RGB Median', imgBGRMedian)
    #cv2.imshow('video RGB Dilatada', imgBGRDil)
    
    key = cv2.waitKey(10)
    if key == 32:  
        break