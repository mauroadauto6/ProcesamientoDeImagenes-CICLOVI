import cv2
import pickle
import numpy as np

# Definir los rangos de color para los asientos rojos y grises en formato BGR
red_lower = np.array([0, 0, 150])
red_upper = np.array([100, 100, 255])
gray_lower = np.array([150, 150, 150])
gray_upper = np.array([220, 220, 220])

asientos = []
with open('biblioteca-pkl/biblioteca.pkl', 'rb') as file:
    asientos = pickle.load(file)

video = cv2.VideoCapture('biblioteca-deteccion/biblioteca.mp4')


while True:
    check, img = video.read()

    for x, y, w, h in asientos:
        espacio = img[y:y+h, x:x+w]
        
        # Convertir el espacio a formato HSV
        espacio_hsv = cv2.cvtColor(espacio, cv2.COLOR_BGR2HSV)
        
        # Calcular las máscaras para los colores rojo y gris
        mask_red = cv2.inRange(espacio, red_lower, red_upper)
        mask_gray = cv2.inRange(espacio, gray_lower, gray_upper)

        # Contar los píxeles en cada máscara
        count_red = cv2.countNonZero(mask_red)
        count_gray = cv2.countNonZero(mask_gray)
        
        other_color = w * h - (count_gray + count_red)
        
        gen_count = w * h

        cv2.putText(img, ('Red: ' + str(count_red)), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(img, ('Gray: ' + str(count_gray)), (x, y + h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, ('General: ' + str(gen_count)), (x, y + h - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(img, ('Other color: ' + str(other_color)), (x, y + h - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        if count_red > 300:
            if count_red < 4200:
                cv2.putText(img, 'OCUPADO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            else:
                cv2.putText(img, 'VACIO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        else:
            if count_gray < 3000:
                cv2.putText(img, 'OCUPADO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            else:
                cv2.putText(img, 'VACIO', (x, y + h - w), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
        
    cv2.imshow('video', img)
    
    key = cv2.waitKey(10)
    if key == 32:
        break