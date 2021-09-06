import cv2 as cv
import cv2
import numpy as np
import math



# kernels de  tranformaciones morfologicas
kernelElliptico = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
kernelCuadrado = np.ones((5,5),np.uint8)

# Tracker de objetos
objetos= {}
contador_objetos = 0
id_count = 0


# Funciones
def update_objetos(detections):
    global id_count
    global objetos
    global contador_objetos

    rectParaDibujar = []
    for objeto in detections:
        x, y, w, h = objeto
        cx = (x+ w//2)
        cy = (y + h//2)

        mismo_objeto = False
        for id, pt in objetos.items():
            dist = math.hypot(cx-pt[0],cy-pt[1])


            if dist < 10:

                if (cx >= 50 and pt[0] < 50):
                    contador_objetos += 1;
                

                objetos[id] = (cx,cy)
                print(objetos[id],id)
                rectParaDibujar.append( [x,y,w,h,id] )
                mismo_objeto = True
                break
        
        # New object is detected we assign the ID to that object
        if mismo_objeto is False:
            objetos[id_count] = (cx, cy)
            rectParaDibujar.append([x, y, w, h, id_count])
            id_count += 1

    new_objetos = {}
    for rect in rectParaDibujar:
        _, _, _, _, object_id = rect
        center = objetos[object_id]
        new_objetos[object_id] = center

    #Update dictionary with IDs not used removed
    objetos = new_objetos.copy()

    return rectParaDibujar


def dibujar_objetos(rectParaDibujar):
    for rect in rectParaDibujar:
        x,y,h,w,id = rect
        cv2.rectangle(frame, (x+250, y+115), ((x + w)+250, (y + h)+115), (0, 255, 0), 2)
        cv2.putText(frame, str(contador_objetos),(50,50),cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0),2)




def circularidad(contorno):
    perimetro = cv2.arcLength(contorno, True)
    area = cv2.contourArea(contorno)
    return (perimetro**2)/(4*np.pi*area)

def preprocessing (image):
    _ ,threshold = cv2.threshold(image,230,255, cv2.THRESH_BINARY)
    
    opening = cv2.morphologyEx(threshold,cv2.MORPH_OPEN, kernelElliptico)
    return opening


# ret, frame = capture.read()
path = './varilla_images/image285.jpg'
frame = cv2.imread(path)
# Terminar while si no hay ninguna imagen
# if frame is None:
#     break
heightFrame, widthFrame, channels = frame.shape
frameR = frame[:,:,0]
roi = frameR[115:185,250:350]
roiH, roiW = roi.shape
frame_prep = preprocessing(roi)
contours, _ = cv2.findContours(frame_prep, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
currentDetections = []
for cont in contours:
    area = cv2.contourArea(cont)
    circ = circularidad(cont)
    if (area < 150 and area > 10) :
        x,y,w,h = cv2.boundingRect(cont)
        currentDetections.append([x,y,w,h])
rectParaDibujar = update_objetos(currentDetections)
dibujar_objetos(rectParaDibujar)
cv2.line(frame,((int(roiW/2)+250),115),((int(roiW/2)+250),roiH+115),(255,0,0),2)




cv2.imshow('thres', frame_prep)
cv2.resizeWindow('thres', roiW*2,roiH*2)
cv2.imshow('Frame', frame)
key = cv.waitKey(0)
# esc = 27
# if key == esc:
#     break



# capture.release()
cv2.destroyAllWindows()