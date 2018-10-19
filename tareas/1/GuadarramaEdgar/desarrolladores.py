#Guadarrama Flores Edgar Alejandro

hackers = 0 #inicializo el numero de hackers en cero porque aun no llega nadie a formarse
serfs = 0 #De la misma manera a los serfs
mutex = Semaphore(1)
colaHack = Semaphore(0)  #Para controlar el numero de hackers que pasan
colaMicro = Semaphore(0) #Controlar el numero de serfs que pasan
Balsa = Semaphore(1)
pasaje = 0

def hacker(id):
    mutex.acquire()
    hackers += 1 #Se suma los hackers
    if hackers == 4:  # la suma de hackers llega a 4 y se mete al ciclo
        hackers -= 4  # Se resta cuatro para reiniciar
        mutex.release()
        subir() #Invoca la funcion

    elif (hackers == 2 and serfs >= 2):  #
        hackers -= 2  # Resta la cola de hackers en 2
        serfs -= 2 #resta la cola de serfs en 2
        subir()  #Invoca la funcion
    else:#
        colaHack.acquire()
        subir()  #Invoca la funcion

#Esta funcion tiene la misma estructura que la de los hackers
def serf(id):
    mutex.acquire()
    serfs += 1
    if serfs == 4:
        colaMicro.acquire()
        serfs -= 4
        mutex.release()
        subir()
    elif (hackers >= 2 and serfs == 2):
        colaHack.release()
        colaMicro.release()
        hackers -= 2
        serfs -= 2
        mutex.release()
        subir()
    else:
        mutex.release()
        colaMicro.acquire()
        subir()

def subir(id):   #Funcion para ascenso de hackers (Imprimir si sube un hacker)
    global pasaje
    Balsa.acquire()
    pasaje += 1
    print("Soy un %d y estoy abordo"(id, hacker))
    print("Soy un %d y estoy abordo"(id, serf))

    if pasaje == 4: #Con la balsa llena se va la balsa
        zarpar() #llama a la funcion
        pasaje = 0  #Reinicia la balsa
    Balsa.release()

def zarpar():
    print("La balsa se mueve hacia la conferencia sin peleas, con cuatro pasajeros")
    sleep(1)

for hacker in range(20):
    Thread(target=hackers, args=[]).start()
    for serf in range(20)
    Thread(target=serfs, args=[]).start()

