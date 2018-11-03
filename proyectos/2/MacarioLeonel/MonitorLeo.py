#!/usr/bin/python https://stackoverflow.com/questions/2429511/why-do-people-write-the-usr-bin-env-python-shebang-on-the-first-line-of-a-pyt
# coding=utf-8 https://www.python.org/dev/peps/pep-0263/

#                                        LEONEL MACARIO FALCON	
#                                     PROYECTO DE SISTEMAS OPERATIVOS 	

from threading import Semaphore, Thread 
import os, threading, time
import commands
mutex = threading.Semaphore(1)
band = 0
tempecpu=0
#Creamos las funciones que hacen las llamadas al sistema y las muestra. 

def cpu_info():
	'''Informacion de CPU'''
	global mutex
	mutex.acquire()
	print " "
	print "*---------------------->>  Informacion del CPU <<----------------------*"
	print " "
	os.system("cat /proc/cpuinfo")
	mutex.release()

def TempCPU():
	'''Temperatura del CPU'''
	global mutex
	mutex.acquire()
	print " "
	print "---------------------->>  TEMPERATURA DEL CPU <<----------------------*"
	print " "
	tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    	cpu_temp = tempFile.read()
    	tempFile.close()
    	return float(cpu_temp)/1000
mutex.release()

def procesos():
	'''Impresión de Procesos'''
	global mutex
	mutex.acquire()
	print " "
	print "*---------------------->>  PROCESOS ACTIVOS <<----------------------*"
	print " "
	os.system("ps -auf")
mutex.release()

#                                            EN CASO DE TENER GPU
#def TempGPU():
#	'''Temperatura del GPU'''
#	global mutex
#	mutex.acquire()
#	print "---------------------->>  TEMPERATURA DEL GPU <<----------------------*"
#    tempFilegpu = open( "/sys/class/thermal/thermal_zone0/temp")
#    	gpu_temp = tempFilegpu.read()
#    	tempFile.close()
#    	return float(cpu_temp)/1000
#mutex.release()

def Memoria():
	'''MEMORIA EN USO'''
	global mutex	
	mutex.acquire()
	print " "
	print "*---------------------->> MEMORIA EN USO <<----------------------*"
	print " "
	os.system("free -h")
	os.system("cat /proc/meminfo")
mutex.release()

def Aviso(): #Por defautl me manda un aviso de que hay un exceso de temperatura a los 40 grados. 
	'''Exceso de temperatura'''
	global mutex
	mutex.acquire()
	tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    	cpu_temp = tempFile.read()
    	tempFile.close()
	if cpu_temp > 40:
		print " "
		print "||||||||||||||||||||||||||||||||||   AVISO   ||||||||||||||||||||||||||||||||||||||||||"
		print "*---------------------->> LA COSA YA SE PUSO COLOR DE HORMIGA <<----------------------*"
		print "*---------------------->> CONECTA UN VENTILADOR EXTERNO       <<----------------------*"
		print " "
mutex.release()


# HILOS PARA CORRESPONDIENTES A CADA FUNCION 
def hilos():
	'''Creación de Hilos'''
	thr0 = threading.Thread(target = TempCPU)
	thr0.start()
	thr1 = threading.Thread(target = Aviso)
	thr1.start()
	thr2 = threading.Thread(target = cpu_info)
	thr2.start()
	thr3 = threading.Thread(target = procesos)
	thr3.start()
	thr4 = threading.Thread(target = Memoria)
	thr4.start()                                      
	#thr5 = threading.Thread(target = TempGPU)   EN CASO DE TENER GPU 
	#thr5.start()  


def command(var):
	'''Lanzador de Hilos'''
	global band 
	if var == "Mostrartodo":
		hilos()
	elif var == "TemperaturaCPU":
		thr = threading.Thread(target = TempCPU)
		print "Temperatura CPU: ", round(TempCPU())
		thr.start()
		thr = threading.Thread(target = Aviso)
		thr.start()
	elif var == "InformacionCPU":
		thr = threading.Thread(target = cpu_info)
		thr.start()
	elif var == "Procesosactivos":
		thr = threading.Thread(target = procesos)
		thr.start()
	elif var == "Memoriaenuso":
		thr = threading.Thread(target = Memoria)
		thr.start()
	#elif var == "TemperaturaGPU":
	#	thr = threading.Thread(target = TempGPU)
	#print "Temperatura GPU: ", round(get_gpu_temp())             EN CASO DE TENER GPU
	#	thr.start()
	#
	elif var == "exit":
		print "*---------------------->> ADIOS <<----------------------*"
		band = 1
	else:
		print "Opcion no encontrada"

def main():
	'''Funciones del programa'''
	global var,mutex 
	os.system("clear")
	while band == 0:
		time.sleep(.1)
		print " "
		print " "
		print "*------------------------------>> OPCIONES <<------------------------------*"
		print " 1.- Para mostrar la temperatura del Procesador, escriba: TemperaturaCPU"
		print " 2.- Para mostrar informacion del CPU, escriba: InformacionCPU"
		print " 3.- Para mostrar los procesos activos, escriba: Procesosactivos"
		print " 4.- Para mostrar la memoria en uso, escriba: Memoriaenuso"
		print " 5.- Para mostrar la temperatura del GPU, escriba (leer documentacion): TemperaturaGPU"
		print " 6.- Para mostrar todas las opciones anteriores: Mostrartodo"
		print " "
		print " "
		print " Para salir, escriba: exit"

		var = raw_input("iNSERTAR OPCION: ")
		command(var)
	mutex.release()

main()