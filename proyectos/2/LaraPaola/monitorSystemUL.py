# *-* encoding: utf-8 *-*
#Hecho por Brenda Paola Lara Moreno
#Sistop-2019-1|FI-UNAM|iPaw
# 11 - Octubre - 2018
# Proyecto 2
#Lenguaje: Python
#Este trabajo se desarrollo en la version 2.7.10
#Para ejecutarlo requiere de Python, y ejecutarlo desde la terminal posisionandose en
#el directorio donde se encuentre guardado el archivo y
#posteriormente ejecutarlo de la sig manera ----> python monitorSystemUL.py
#Funciona correctamente en sistemas UNIX/LINUX

import threading
import time
import commands

semaforo = threading.Semaphore(0)
mensaje = "\nEspere 10 segundos para regresar automaticamente al menu\n"

def Procesador():
    print "\t »------(¯` Informacion del Procesador ´¯)------»\n\n"
    modelo = commands.getoutput("cat /proc/cpuinfo | grep \"model name\"")
    numNucleos = commands.getoutput("cat /proc/cpuinfo | grep \"cpu cores\"")
    tamCache = commands.getoutput("cat /proc/cpuinfo | grep \"cache size\"")

    print "El modelo de procesador es:\n\n" + modelo + "\n"
	print "El numero de nucleos es:\n\n" + nucleos + "\n"
	print "La cantidad de cache es:\n\n" + cache + "\n"
	print mensaje
    time.sleep(10) #Tiempo establecido para terminar el proceso y regresar automaticamente al menu
    semaforo.release()
    return 0

def Sistema():
	print(chr(27) + "[2J")
	datos = commands.getoutput('cat /proc/version') #Obtiene los datos del sistema
	print datos #muestra los datos obtenidos
	print mensaje #muestra mensaje de espera para finalizar el proceso
	time.sleep(10) #Tiempo establecido para terminar el proceso y regresar automaticamente al menu
	semaforo.release()
	return 0


def Memoria():
	print(chr(27) + "[2J")
	print "\t »------(¯` Informacion de Memoria ´¯)------»\n\n"
	aux = 0
	#Obtencion de datos
	memTotal=commands.getoutput('cat /proc/meminfo|grep "MemTotal:"|tr -s "'" "'"|cut -d "'" "'" -f 2')
	memLibre=commands.getoutput('cat /proc/meminfo|grep "MemFree:"|tr -s "'" "'"|cut -d "'" "'" -f 2')
	memDisp=commands.getoutput('cat /proc/meminfo|grep "MemAvailable:"|tr -s "'" "'"|cut -d "'" "'" -f 2')
	swapTotal=commands.getoutput('cat /proc/meminfo|grep "SwapTotal:"|tr -s "'" "'"|cut -d "'" "'" -f 2')
	swapLibre=commands.getoutput('cat /proc/meminfo|grep "SwapFree:"|tr -s "'" "'"|cut -d "'" "'" -f 2')

	aux = int(mTotal)
	memTotal = str(aux)
	aux = int(memLibre)
	memLibre = str(aux)
	memOcu = str(int(memTotal) - int(memLibre))
#Se imprimen los datos obtenidos
	print "\n-- Memoria -- \n"
	print "\nMemoria Disponible: " + memDisp
	print "\nMemoria Ocupada: " + memOcu
	print "\nMemoria Total: " + memTotal
	print "\n-- Swap -- \n"
	print "\nSwap Total: " + swapTotal
	print "\nSwap Libre: " + swapLibre
    print mensaje #muestra mensaje de espera para finalizar el proceso
	time.sleep(10) #Tiempo establecido para terminar el proceso y regresar automaticamente al menu
	semaforo.release()
	return 0

# Funcion de un menu para la interaccion con el programa
def Menu():
	global semaforo
	op = '0'
	while op != '4':
		print(chr(27) + "[2J")
		opciones = {'1':Procesador,'2':Sistema, '3': Memoria}
		print "Elije una opcion. "
		print "\n 1) Informacion del Procesador"
		print "\n 2) Informacion del Sistema."
		print "\n 3) Informacion de la Memoria."
		print "\n 4) Salir"
		op = raw_input('\nSelecciona una opción: \n')
		try:
			res = opciones[op]()
			semaforo.acquire()
		except:
			if op != '4':
				print("Error!, Ingresa una opcion valida")
Menu()
