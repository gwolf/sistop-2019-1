#!/usr/bin/python3
from threading import Semaphore, Thread
from time import sleep
from random import random

def hazlo(id_hilo, sem):
    print("Hilo %d iniciando" % id_hilo)
    sleep(random())
    sem.acquire()
    print("Hilo %d: Dentro de la seccion critica" % id_hilo)
    sleep(random())
    print("Hilo %d: Dejando la seccion critica" % id_hilo)
    sem.release()

sem = Semaphore(2)
for i in range(1,10):
    Thread(target=hazlo, args=[i, sem]).start()

