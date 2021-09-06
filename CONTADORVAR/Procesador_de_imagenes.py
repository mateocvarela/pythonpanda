import cv2
import numpy as np



class ProcesadorImagenes:
    def __init__(self, imagen):
        self.imagen = imagen
        self.contornos = None


    def preprocesar_imagen (self, umbral, kernelOp):
        self.binarizar_imagen(umbral, 255)
        self.opening_imagen(kernelOp)
        return self.imagen

    def binarizar_imagen(self, umbral, valorMaximo):
        _ , self.imagen = cv2.threshold(self.imagen, umbral,valorMaximo, cv2.THRESH_BINARY) 
        return self.imagen
    
    def opening_imagen (self, kernel):
        self.imagen = cv2.morphologyEx(self.imagen, cv2.MORPH_OPEN, kernel)
        return self.imagen


    def recortar_imagen(self, ROI):
        self.imagen = self.imagen[ROI[0]:ROI[1],ROI[2]:ROI[3]]
        return self.imagen

    def dibujar_linea_imagen(self, punto1, punto2):
        self.imagen = cv2.line(self.imagen,punto1,punto2, (255,0,0), 2)
        return self.imagen

    def canal_imagen(self, canal):
        self.imagen = self.imagen[:,:,canal]
        return self.imagen

    def extraer_contornos_imagen(self):
        self.contornos, _ = cv2.findContours(self.imagen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return self.contornos

    def dibujar_rectangulos (self,rectangulos, contador_objetos):
        for rectangulo in rectangulos:
            x,y,h,w,id = rectangulo
            cv2.rectangle(self.imagen, (x+250, y+115), ((x + w)+250, (y + h)+115), (0, 255, 0), 2)
            cv2.putText(self.imagen, str(contador_objetos),(50,50),cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0),2)

    def get_imagen(self):
        return self.imagen