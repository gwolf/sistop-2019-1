# Nota: presionar enter después de que la info sea desplegada para limpiar la pantalla y volver al menú
# La función red puede tomar un poco de tiempo en ejecutarse por completo

from threading import Semaphore, Thread
import os, threading

#se utilizara para lograr la sincronización de los hilos 
mutex = threading.Semaphore(1)


def switch_Op(opcion):
	if opcion == '1':
		#Procesos
		x = threading.Thread(target = procesos)
		x.start()
	
	elif opcion == '2':
		#Memoria
		x = threading.Thread(target = memoria)
		x.start()

	elif opcion == '3':
		#CpuInfo
		x = threading.Thread(target = cpuInfo)
		x.start()

	elif opcion == '4':
		#Temperatura
		x = threading.Thread(target = temperatura)
		x.start()
	
	elif opcion == '5':
		#Muestra Todo
		hilo()
	elif opcion == '6':
		x = threading.Thread(target = red)
		x.start()
	elif opcion == '7':
		#Salir
		print("\nHasta luego!\n")
		exit()
		
#Funciones
def main():
	global mutex, opcion
	
	while True:
		os.system("clear")
		print ("Seleccione una opcion: \n1) Procesos \n2) Memoria \n3) Cpuinfo \n4) Temperatura \n5) Todo \n6) Red \n7) Salir")
		opcion = input('Ingrese opcion: ')
		switch_Op(opcion)

def procesos():
	global mutex
	mutex.acquire()
	print("\n-----------------------------------Procesos----------------------------------\n\n")
	os.system("ps -auf")
	mutex.release()

def temperatura():
	global mutex
	mutex.acquire()
	print("\n----------------------------------Temperatura---------------------------------\n\n")
	os.system("sensors")
	mutex.release()

def cpuInfo():
	global mutex
	mutex.acquire()
	print("\n------------------------------------CPUinfo----------------------------------\n\n")
	os.system("cat /proc/cpuinfo")
	mutex.release()


def memoria():
	global mutex
	mutex.acquire()
	print("\n------------------------------------Memoria-----------------------------------\n\n")
	os.system("free -h")
	os.system("cat /proc/meminfo")
	mutex.release()

def red():
	global mutex
	mutex.acquire()
	print("\n---------------------------------------red------------------------------------\n\n")
	os.system("netstat -a")
	mutex.release()


def hilo():
	
	h1 = threading.Thread(target = procesos)
	h1.start()
	h2 = threading.Thread(target = memoria)
	h2.start()
	h3 = threading.Thread(target = temperatura)
	h3.start()
	h4 = threading.Thread(target = cpuInfo)
	h4.start()
	h5 = threading.Thread(target = red)
	h5.start()
	

main()
