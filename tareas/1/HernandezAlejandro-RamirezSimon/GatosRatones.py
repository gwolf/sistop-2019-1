from threading import Thread,Semaphore
from time import sleep
from random import randint

def conta(self):
    self.plato = Semaphore(5)
    self.mutContador = Semaphore(1)
    self.gatosComiendo = 0
    self.ratonesComiendo = 0
    self.atrapado = 0

def comerGato(self):
    print("Aparece un gato\n")
    c.plato.acquire()
    c.mutContador.acquire()
    c.gatosComiendo += 1
    print("Gato comiendo\n")
    self.hambre = randint(1,20)
    c.mutContador.release()
    while self.hambre != 0:
        c.mutContador.acquire()
        if c.ratonesComiendo > 0:
            print("Gato se come un raton")
            c.atrapado = 1
        self.hambre += -1
        c.mutContador.release()
    c.mutContador.acquire()
    print("Gato termina de comer")
    c.gatosComiendo += -1
    c.plato.release()
    c.mutContador.release()


def comerRaton(self):
    print("Aparece un raton\n")
    c.plato.acquire()
    c.mutContador.acquire()
    c.ratonesComiendo += 1
    print("Raton comiendo")
    self.hambre = randint(1,20)
    c.mutContador.release()
    while self.hambre != 0:
        c.mutContador.acquire()
        if c.atrapado == 1:
            c.mutContador.release()
            break
        self.hambre += -1
        c.mutContador.release()
    c.mutContador.acquire()
    if self.hambre == 0:
        print("Raton termina de comer")
    c.ratonesComiendo += -1
    c.plato.release()
    c.mutContador.release()

c = conta(1)

for g in range(0,1):
    Thread(target = comerGato, args = [g]).start()

for r in range(0,1):
    Thread(target = comerRaton, args = [r]).start()

