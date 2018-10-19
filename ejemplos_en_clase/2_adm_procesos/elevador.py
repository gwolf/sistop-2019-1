#!/usr/bin/python3
from threading import Semaphore, Thread
from time import sleep
from random import random,choice

pisos = [i for i in range(0,5)]
# Nombres y apellidos: De la lista del semestre 2019-1
nombres = ["Alberto", "Alejandro", "Andrew", "Ángel", "Anibal", "Ascary",
           "Blaise", "Brenda", "Cristian", "Edgar", "Eduardo", "Efrén", "Emma",
           "Guadalupe", "Inri", "Israel", "Javier", "Jesús", "José", "Karla",
           "Laura", "Leonel", "Lizeth", "Luis", "Manuel", "María", "Miguel",
           "Orlando", "Oscar", "Paola", "Patricia", "Rodolfo", "Simon",
           "Yerenia", "Yesenia"]
apellidos = ["Aceves", "Acuña", "Aguilar", "Alejandro", "Amado", "Ancona",
             "Barcena", "Barrios", "Bautista", "Buendía", "Camacho",
             "Carachure", "Ceseña", "Chibras", "Coronel", "Espinosa",
             "Espinoza", "Facio", "Facundo", "Falcón", "Flores", "Fuentes",
             "García", "Guadarrama", "Guillermo", "Guzmán", "Hernández",
             "Jiménez", "Lara", "Macario", "Madrid", "Medina", "Mena",
             "Monroy", "Moreno", "Morua", "Negrete", "Pérez", "Ramírez",
             "Rodríguez", "Ruiz", "Sánchez", "Tolentino", "Trejo", "Valeriano",
             "Velasco", "Vera", "Vázquez", "Zagal"]

'''
Una Persona sólo existe para nosotros cuando existe en relación con
el elevador: Cuando quiere ir de un piso al otro. Fuera de la
verificación mínima de sanidad, es simple: Aparece, se forma en la cola
de entrada, se forma en la cola de destino, llega a su destino.
'''
class Persona:
    def __init__(self, elev):
        self.nombre = '%s %s' % (choice(nombres), choice(apellidos))
        self.origen = choice(pisos)
        # Evitamos que vayan al mismo piso donde ya están
        self.quedan = pisos[:]
        self.quedan.remove(self.origen)
        self.destino = choice(self.quedan)

        print("** %20s: del piso %s al piso %s" %
              (self.nombre, self.origen, self.destino))
        elev.cola_espera(self.origen).forma(self)
        elev.cola_dest(self.destino).forma(self)
        print("%20s se baja del elevador en el piso %s" % (self.nombre, self.destino))


'''
El funcionamiento del elevador es también bastante sencillo: Inicializa
las estructuras necesarias. Separamos "anda" de la inicialización porque
es una buena "manija" para crear un hilo; se mantiene como un ciclo infinito
revisando las colas y la capacidad, viendo si hay gente que pueda subir y bajar
(revisando capacidades), avanzando en la dirección que corresponda...

El elevador implementa dos colas por cada piso: Una cola de espera (para las
personas que esperan para subir al elevador) y una cola de destino (para
quienes están ya en el elevador y quieren llegar a determinado piso).
'''
class Elevador:
    def __init__(self):
        # Todos los ingenieros canónicos están definidos con el mismo
        # peso
        self.capacidad = 6
        self.a_bordo = 0
        # El elevador "nace" naturalmente en el piso más bajo
        self.piso = pisos[0]
        # 1 = arriba, 0 = abajo
        self.direccion = 1
        # Cada cola de un elevador es un semáforo. Pero para evitar
        # esperas eternas en lo que se llena un elevador, también
        # indicamos cuántas persoans están esperando en cada piso
        self.colas_espera = [Cola('E', i) for i in pisos]
        self.colas_dest = [Cola('D', i) for i in pisos]

    def anda(self):
        while True:
            while self.a_bordo < self.capacidad and self.colas_espera[self.piso].esperando() > 0:
                self.colas_espera[self.piso].saca()
                self.a_bordo += 1
            self.avanza()

    def avanza(self):
        # No bajar debajo del piso, ni subir arriba del techo
        if self.piso == pisos[0] and self.direccion == 0:
            self.direccion = 1
        if self.piso == pisos[-1] and self.direccion == 1:
            self.direccion = 0

        siguiente = self.piso+1 if self.direccion == 1 else self.piso-1
        print('E %s %d→%d (%d pas) Colas: %s' %
              ( '↑' if self.direccion==1 else '↓', self.piso, siguiente,
                self.a_bordo, self.estado_colas()))
        self.piso = siguiente
        sleep(1)
        while self.colas_dest[self.piso].esperando() > 0:
            self.colas_dest[self.piso].saca()
            self.a_bordo -= 1

    def cola_espera(self,piso):
        return self.colas_espera[piso]

    def cola_dest(self,piso):
        return self.colas_dest[piso]

    def estado_colas(self):
        res = 'Espera:'
        for e in self.colas_espera:
            res += '%3d' % e.esperando()
        res += ' Destino:'
        for d in self.colas_dest:
            res += '%3d' % d.esperando()
        return res

'''
Toda la lógica de sincronización se implementa dentro de esta clase (y por lo
mismo, podríamos llamarle un "monitor"). "forma" es invocado por cada Persona,
y "saca" es invocado por el Elevador, y de esa manera se sincronizan.
'''
class Cola:
    def __init__(self, tipo, piso):
        self.piso = piso
        self.tipo = tipo
        self.personas = Semaphore(0)
        self.num_personas = 0
        self.mut_personas = Semaphore(1)

    def forma(self, persona):
        print("C%s%d (%d p) << %s" %
              (self.tipo, self.piso, self.num_personas, persona.nombre))
        self.mut_personas.acquire()
        self.num_personas += 1
        self.mut_personas.release()
        self.personas.acquire()

    def saca(self):
        print("C%s%d (%d p) >>" %
              (self.tipo, self.piso, self.num_personas))
        self.mut_personas.acquire()
        self.num_personas -= 1
        self.mut_personas.release()
        self.personas.release()

    def esperando(self):
        return self.num_personas

elev = Elevador()
Thread(target = elev.anda, args = ()).start()

while True:
    Thread(target=Persona, args=[elev]).start()
    sleep(1)
