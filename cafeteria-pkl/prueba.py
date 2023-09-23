import cv2
import numpy as np
import pickle

img = cv2.imread('cafeteria-pkl/ss-cafeteria.png')

while True:
    
    """                    BGR TO GRAY                            """
    imgBGR2GRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBGRTH = cv2.adaptiveThreshold(imgBGR2GRAY, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgBGRMedian = cv2.medianBlur(imgBGRTH, 5)
    kernelBGR = np.ones((5,5), np.int8)
    imgBGRDil = cv2.dilate(imgBGRMedian, kernelBGR)
    
    #cv2.imshow('BGR TO GRAY', imgBGR2GRAY)
    #cv2.imshow('BGR-GRAY TH', imgBGRTH)
    cv2.imshow('video BGR Median', imgBGRMedian)
    #cv2.imshow('video BGR Dilatada', imgBGRDil)
    
    """                    RGB TO GRAY                            """
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB2GRAY = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2GRAY)
    imgRGBTH = cv2.adaptiveThreshold(imgRGB2GRAY, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgRGBMedian = cv2.medianBlur(imgRGBTH, 5)
    kernelRGB = np.ones((5,5), np.int8)
    imgRGBDil = cv2.dilate(imgRGBMedian, kernelRGB)

    #cv2.imshow('RGB TO GRAY', imgRGB2GRAY)
    #cv2.imshow('RGB-GRAY TH', imgRGBTH)
    cv2.imshow('video RGB Median', imgRGBMedian)
    #cv2.imshow('video RGB Dilatada', imgRGBDil)
    
    key = cv2.waitKey(100)
    if key == 32:  # 32 es el código ASCII de la barra espaciadora
        break