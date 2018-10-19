#!/usr/bin/python3
#
# El programa simplemente lanza varios hilos que van a realizar
# trabajo de muuuy poca relevancia. Pero podemos ver, utilizando
# pmap, que cada hilo crea un stack.

from threading import Thread
from time import sleep

def vida_de_hilo(num):
    print("Hilo %d iniciando" % num)
    while True:
        print("%d" % num)
        sleep(5)

for i in range(1,10):
    Thread(target=vida_de_hilo, args=[i]).start()
    sleep(2)
