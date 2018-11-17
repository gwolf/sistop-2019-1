
from threading import Semaphore, Thread
from time import sleep
from random import random,choice




def Asesoria(id_estudiante, cubiculo, profesor):
	


	print("\tllego el Estudiante %d" % id_estudiante)
	sleep(random())
	cubiculo.acquire()	# semáforo que permite regular que solo 3 alumnos estén dentro del cubículo
	pregunta = choice(range(1,5))
	print(">> Estudiante %d Entra al cubículo y tiene %d dudas" % (id_estudiante, pregunta))
	
	while (pregunta > 0):
		sleep(random())
		profesor.acquire()  # lo uso como torniquete que solo permite que uno de los estudiantes dentro del cubículo haga su pregunta
		print("\tDuda %d resuelta a Estudiante %d" % (pregunta, id_estudiante))
		pregunta = pregunta -1
		profesor.release()
		sleep(random())


	print("<< Estudiante %d: Abandonando el cubículo" % id_estudiante)
			
	cubiculo.release()
		
print("El profesor duerme")

cubiculo = Semaphore(3) #cantidad máxima de alumnos dentro del cubículo
profesor = Semaphore(1)	#solo responde a un alubno a la vez 
i=0
while True:
	i=i+1
#for i in range(1,10):
	Thread(target=Asesoria, args=[i, cubiculo, profesor]).start()
	sleep(1)
