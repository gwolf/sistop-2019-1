from random import random
from time import sleep
import threading
lectores = 0
mutex = threading.Semaphore(1)
cuarto_vacio = threading.Semaphore(1)
torniquete = threading.Semaphore(1)

def escritor(id):
    sleep(random())
    print("   Escritor %d iniciando" % id)
    torniquete.acquire()
    print("   Escritor %d: En el torniquete" % id)
    cuarto_vacio.acquire()
    print("   Escritor %d: El cuarto es mío!" % id)
    escribe(id)
    cuarto_vacio.release()
    torniquete.release()
    print("   Escritor %d se fue" % id)

def lector(id):
    sleep(random())
    global lectores
    print("Lector %d iniciando" % id)
    torniquete.acquire()
    torniquete.release()
    
    mutex.acquire()
    lectores = lectores + 1
    print("%d: Ahora somos %d lectores" % (id, lectores))
    if lectores == 1:
        print("%d: El cuarto estaba vacío" % id)
        cuarto_vacio.acquire()
    mutex.release()
    
    lee(id)
    
    mutex.acquire()
    lectores = lectores - 1
    print("%d: Ya me voy, dejo %d lectores" % (id, lectores))
    if lectores == 0:
      cuarto_vacio.release()
      print("%d: Dejo un cuarto vacío"% id)
    mutex.release()

def lee(id):
    print("El lector %d está leyendo..." % id)
    sleep(0.3)
    print("%d ya terminó de leer" % id)

def escribe(id):
    print("   El escritor %d está escribiendo.." % id)
    sleep(2)
    print("   %d terminó de escribir" % id)

for escr in range(3):
    threading.Thread(target = escritor, args = [escr]).start()
for lect in range(20):
    threading.Thread(target = lector, args = [lect]).start()
