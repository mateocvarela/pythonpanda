import cv2 as cv
import cv2
import numpy as np
import Procesador_de_imagenes as imageProcesing
import tracker as tracking

capture = cv.VideoCapture('varillasPlanta.mp4')

# kernels de  tranformaciones morfologicas
SQUARE_KERNEL = np.ones((5,5),np.uint8)
ELLIPTICAL_KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4)) 

rastreador_de_objetos = tracking.Tracker() 


# def dibujar_objetos(rectParaDibujar):
#     for rect in rectParaDibujar:
#         x,y,h,w,id = rect
#         cv2.rectangle(frame, (x+250, y+115), ((x + w)+250, (y + h)+115), (0, 255, 0), 2)
#         cv2.putText(frame, str(contador_objetos),(50,50),cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0),2)

def filtrar_contornos(contornos):
    currentDetections = []
    for cont in contornos:
        area = cv2.contourArea(cont)
        #circ = circularidad(cont)
        #print("area",area)
        if ( area > 5 ) :
            x,y,w,h = cv2.boundingRect(cont)
            if w > 15:
                currentDetections.append([x+int(w/2),y,int(w/2),h])
                currentDetections.append([x,y,int(w/2),h])
            elif h > 15:
                currentDetections.append([x,y+int(h/2),w,int(h/2)])
                currentDetections.append([x,y,w,int(h/2)])
            else:
                currentDetections.append([x,y,w,h])
    return currentDetections

# def circularidad(contorno):
#     perimetro = cv2.arcLength(contorno, True)
#     area = cv2.contourArea(contorno)
#     return (perimetro**2)/(4*np.pi*area)


while (1):
    ret, frame = capture.read()
    if frame is None:
        break
    heightFrame, widthFrame, channels = frame.shape
    procesador_frame = imageProcesing.ProcesadorImagenes(frame)

    procesador_thres = imageProcesing.ProcesadorImagenes(frame)
    procesador_thres.canal_imagen(1)
    ROI = (115,185,250,350)
    roiH, roiW = procesador_thres.recortar_imagen(ROI).shape
    procesador_thres.preprocesar_imagen(253,ELLIPTICAL_KERNEL) # Preprocesar hace un threhold y luego un opening

    contours = procesador_thres.extraer_contornos_imagen()
    currentDetections = filtrar_contornos(contours)
    


    rectangulosParaDibujar = rastreador_de_objetos.update_objetos(currentDetections)
    contador_objetos = rastreador_de_objetos.get_idCount()
    procesador_frame.dibujar_rectangulos(rectangulosParaDibujar,contador_objetos)


    punto1_linea = ((roiW//2)+250,115)
    punto2_linea = ((roiW//2)+250,roiH+115)
    procesador_frame.dibujar_linea_imagen(punto1_linea,punto2_linea)
    


    thres = procesador_thres.get_imagen()
    frame = procesador_frame.get_imagen()
    cv2.imshow('thres', thres)
    cv2.resizeWindow('thres', roiW*2,roiH*2)
    cv2.imshow('Frame', frame)
    key = cv.waitKey(30)                
    esc = 27
    if key == esc:
        break



capture.release()
cv2.destroyAllWindows()