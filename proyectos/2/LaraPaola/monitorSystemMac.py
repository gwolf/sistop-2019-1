# *-* encoding: utf-8 *-*
#Hecho por Brenda Paola Lara Moreno
#Sistop-2019-1|FI-UNAM|iPaw
# 11 - Octubre - 2018
# Proyecto 2
#Lenguaje: Python
#Este trabajo se desarrollo en la version 2.7.10
#Para ejecutarlo requiere de Python,desde un equipo con sistema MacOS y ejecutarlo desde la terminal posisionandose en
#el directorio donde se encuentre guardado el archivo y
#posteriormente ejecutarlo de la sig manera ----> python monitorSystemMac.py
#Revisar documentacion en caso de alguna duda

import threading
import time
import commands
import psutil

mensaje = "* Para conocer los significados de la informacion obtenida, favor de consultar documentacion"
semaforo = threading.Semaphore(0)

def Sistema():
	print(chr(27) + "[2J")
	print "\t »------(¯` Informacion de Sistema ´¯)------»\n\n"
	sis = psutil.cpu_times() #Obtiene los datos del CPU
	print sis
	print "\n\n"
	freq = psutil.cpu_freq()
	print  freq
	print "\n\n"
	print mensaje
	print "\n\n\nEspere 10 segundos para regresar automaticamente al menu\n"
	time.sleep(10) #Tiempo establecido para terminar el proceso y regresar al menu
	semaforo.release()
	return 0


def Memoria():
	print(chr(27) + "[2J")
	print "\t »------(¯` Informacion de Memoria ´¯)------»\n\n"
	mem = psutil.virtual_memory() #Obtiene datos de la memoria
	swapmem = psutil.swap_memory()
	print " \n\t---- Memoria -----"
	print mem
	print "\n\t----Swap ----"
	print swapmem
	print "\n\n"
	print mensaje
	print "\n\n\nEspere 10 segundos para regresar automaticamente al menu\n"
	time.sleep(10) #Tiempo establecido para terminar el proceso y regresar al menu
	semaforo.release() #Libera al hilo opcion para regresar al hilo menu
	return 0##



	#Se declara la funcion del menu para interactuar con el software desde la terminal
def Menu():
	global semaforo
	op = '0'
	while op != '3':
		print(chr(27) + "[2J")
		opciones = {'1':Sistema,'2':Memoria}

		print "Elije una opcion. \n"
		print "1) Informacion del sistema.\n"
		print "2) Informacion de la memoria.\n"
		print "3) Salir.\n"
		op = raw_input('\nSelecciona una opción: \n')
		try:
			res = opciones[op]()
			semaforo.acquire()
		except:
			if op != '3':
				print("Opción invalida")
Menu()
