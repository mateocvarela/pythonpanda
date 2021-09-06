import math

POSICION_LINEA = 50

class Tracker:

    def __init__(self):
        self.objetos = {}
        self.id_count = 0
        self.contadorObjetos = 0
    
    def update_objetos(self, detections):

        rectangulosParaDibujar = []
        
        for objeto in detections:
            x, y, w, h = objeto
            posXActual = (x+ w//2)
            posYActual = (y + h//2)
            done = 0

            se_encontro_el_mismo_objeto = False
            for id, posicionYEstado in self.objetos.items():
                posXAnterior = posicionYEstado[0]
                posYAnterior = posicionYEstado[1]
                done = posicionYEstado[2]
                if self.objetos_son_el_mismo((posXActual,posYActual),(posXAnterior,posYAnterior)):
                    if done == 0:
                        done = self.objeto_paso_por_linea(posXAnterior, posXActual)
                    self.objetos[id] = (posXActual,posYActual, done)
                    rectangulosParaDibujar.append( [x,y,w,h,id] )
                    se_encontro_el_mismo_objeto = True
                    break
            
            if se_encontro_el_mismo_objeto is False:
                self.objetos[self.id_count] = (posXActual, posYActual, 0)
                rectangulosParaDibujar.append([x, y, w, h, self.id_count])
                self.id_count += 1
        
        self.limpiar_objetos(rectangulosParaDibujar)

        return rectangulosParaDibujar


    def limpiar_objetos(self, rectangulosParaDibujar):
        new_objetos = {}
        for rect in rectangulosParaDibujar:
            _, _, _, _, object_id = rect
            puntoYEstado = self.objetos[object_id]
            new_objetos[object_id] = puntoYEstado             
        #Update dictionary with IDs not used removed
        self.objetos = new_objetos.copy()


    def objeto_paso_por_linea(self, posicionXAnterior, posicionXActual ):
        if (posicionXActual >= POSICION_LINEA and posicionXAnterior < POSICION_LINEA):
            self.contadorObjetos += 1
            newDone = 1
        else:
            newDone = 0
        return newDone

    def objetos_son_el_mismo(self, coordenadasActuales, coordenadasAnteriores):
        es_mismo_objeto = True
        if self.puntos_cercanos(coordenadasActuales,coordenadasAnteriores):
            return es_mismo_objeto
        else:
            return not es_mismo_objeto


    def puntos_cercanos(self, coordenadasActuales,coordenadasAnteriores):
        posXActual, posYActual = coordenadasActuales
        posXAnterior, posYAnterior = coordenadasAnteriores
        dist =  math.hypot(posXActual-posXAnterior,posYActual-posYAnterior)
        if dist < 10:
            return True
        else:
            return False

    def get_idCount(self):
        return self.contadorObjetos