from threading import Thread,Semaphore
from time import sleep

def establece_conexion():
    sleep(1)
    print("Ya está establecida la conexión")
    sem.release()

def manda_datos():
    print("Quiero mandar datos")
    sem.acquire()
    print("Enviando datos. ¡Listo!")

sem = Semaphore(0)
Thread(target = manda_datos, args = []).start()
Thread(target = establece_conexion, args=[]).start()

