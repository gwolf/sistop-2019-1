#!/usr/bin/python
# coding=utf-8


#Plantilla de estilo del menú: \033[cod_formato;cod_color_texto;cod_color_fondom

from threading import Semaphore, Thread
from time import sleep
import os, threading, time, datetime


mut_impr = threading.Semaphore(1)	#MUTEX QUE SOLICITAN LOS PROCESOS PARA IMPRIMIR EN PANTALLA
band = 0				#VARIABLE DE CONDICIÓN PARA MANTENER EJECUTANDO EL MONITOR
i=0					#VARIABLE DE CONDICIÓN PARA EL CICLO DE MEMORIA DEL HILO DE MEMORIA
j=0					#VARIABLE DE CONDICIÓN PARA EL CICLO DEL HILO DE PROCESOS

# MENU DEL PROGRAMA
def menu():
	print("\033[1;30;47m"+"COMANDOS: memoria(m) | procesos(p) | disco(d) | logins (l) | cpuinfo(c) | interrupts (i) | help(h) | clear(q) | exit(x)"+'\033[0;m')

# FUNCIÓN QUE MUESTRA EL USO DE DISCO
def uso_disco():
	global mut_impr,i,j
	i=1			#TERMINA EL BUCLE DEL HILO DE MEMORIA
	j=1			#TERMINA EL BUCLE DEL HILO DE MEMORIA
	mut_impr.acquire()	#ADQUIERE EL MUTEX
	print("\033[1;37;42m"+"                                        USO DE DISCO                                        "+'\033[0;m\n')
	print " "
	os.system("du -h")
	mut_impr.release()	#LIBERA EL MUTEX

#FUNCIÓN QUE MUESTRA LOS PROCESOS ACTIVOS
def procesos():
	global mut_impr,i,j
	i=1			#FORZA LA DETENCIÓN DEL BUCLE DEL HILO DE MEMORIA
	mut_impr.acquire()	#-----------ADQUIERE EL MUTEX
	j=0			#SE ASEGURA DE REINICIAR LA VARIABLE PARA INICIAR EL BUCLE
	while j==0:		#INICIA EL BUCLE PARA ACTUALIZAR LA INFORMACIÓN
		os.system("clear")
		print("\033[1;37;42m"+"                                        PROCESOS                                       "+'\033[0;m\n')
		now = datetime.datetime.now()				
		print (now.strftime("Date: %Y-%m-%d %H:%M:%S\n"))	#IMPRIME LA FECHA Y HORA ACTUAL
		os.system("ps -auf")
		menu()
		mut_impr.release()	#----------LIBERA EL MUTEX ANTES DEL SIGUIENTE CICLO
		sleep(0.2)		#DUERME 0.2 SEGUNDOS PARA QUE DE TIEMPO DE QUE OTRO HILO TOME EL MUTEX


#FUNCIÓN QUE MUESTRA EL USO DE MEMORIA
def uso_memoria():
	global mut_impr,i,j
	j=1			#FORZA LA DETENCIÓN DEL BUCLE DEL HILO DE PROCESOS
	mut_impr.acquire()	#-----------ADQUIERE EL MUTEX
	i=0			#SE ASEGURA DE REINICIAR LA VARIABLE PARA INICIAR EL BUCLE
	while i == 0:		#INICIA EL BUCLE PARA ACTUALIZAR LA INFORMACIÓN
		os.system("clear")
		print("\033[1;37;42m"+"                                        MEMORIA                                        "+'\033[0;m\n')
		now = datetime.datetime.now()
		print (now.strftime("Date: %Y-%m-%d %H:%M:%S\n"))	#IMPRIME LA FECHA Y HORA ACTUAL
		os.system("free -h")
		print "____________________________________________________________________________"
		a = open("/proc/meminfo","r")
		for l in a.readline()
			print a.readline()
		menu()
		mut_impr.release()	#----------LIBERA EL MUTEX ANTES DEL SIGUIENTE CICLO
		sleep(0.2)		#DUERME 0.2 SEGUNDOS PARA QUE DE TIEMPO DE QUE OTRO HILO TOME EL MUTEX
	mut_impr.release()
		
#FUNCIÓN QUE MUESTRA LOS LOGINS EN EL SISTEMA OPERATIVO	
def logins():
	
	global mut_impr,i,j
	i=1	#SE FORZA LA DETENCIÓN DE LOS BUCLES 
	j=1
	mut_impr.acquire()	#----------ADQUIERE EL MUTEX
	print("\033[1;37;42m"+"                                        LOGINS                                       "+'\033[0;m\n')
	print " "
	os.system("last")

#FUNCIÓN QUE MUESTRA LA INFORMACIÓN RELACIONADA AL CPU
def cpu_info():

	global mut_impr,i,j
	i=1	#SE FORZA LA DETENCIÓN DE LOS BUCLES 
	j=1
	mut_impr.acquire()	#----------ADQUIERE EL MUTEX
	print("\033[1;37;42m"+"                                        CPU INFO                                        "+'\033[0;m\n')
	print "Tiempo en funcionamiento:"
	a = open("/proc/uptime","r")
		for l in a.readline()
			print a.readline()
	b = open("/proc/cpuinfo","r")
		for l in b.readline()
			print b.readline()

#FUNCIÓN QUE MUESTRA LAS INTERRUPCIONES DEL SISTEMA
def interrupciones():

	global mut_impr,i,j
	i=1	#FORZA LA DETENCIÓN DE LOS BUCLES
	j=1
	mut_impr.acquire()	#----------ADQUIERE EL MUTEX
	print("\033[1;37;42m"+"                                        INTERRUPCIONES                                        "+'\033[0;m\n')
	print " "
	a = open("/proc/interrupts","r")
		for l in a.readline()
			print a.readline()

#FUNCIÓN PARA LIMPIAR LA PANTALLA
def limpia_pantalla():
	'''Limpiar Pantalla'''
	global mut_impr,i,j
	i=1	#FORZA LA DETENCIÓN DE LOS BUCLES
	j=1
	mut_impr.acquire()	#---------ADQUIERE EL MUTEX
	os.system("clear")

#FUNCIÓN QUE LANZA LOS HILOS CONFORME SON SOLICITADOS EN EL SHELL
'''CUANDO EL USUARIO LLAMA A UN HILO, INMEDIATAMENTE LIBERA EL MUTEX
PARA QUE PUEDA ADQUIRIRLO EL HILO EN CUESTIÓN'''
def command(var):
	'''Lanzador de Hilos'''
	global band

	if var == "d":
		mut_impr.release()
		thr = threading.Thread(target = uso_disco)
		thr.start()
	elif var == "m":
		mut_impr.release()
		thr = threading.Thread(target = uso_memoria)
		thr.start()
	elif var == "p":
		mut_impr.release()
		thr = threading.Thread(target = procesos)
		thr.start()
	elif var == "l":
		mut_impr.release()
		thr = threading.Thread(target = logins)
		thr.start()
	elif var == "c":
		mut_impr.release()
		thr = threading.Thread(target = cpu_info)
		thr.start()
	elif var == "i":
		mut_impr.release()
		thr = threading.Thread(target = interrupciones)
		thr.start()
	elif var == "q":
		mut_impr.release()
		thr = threading.Thread(target = limpia_pantalla)
		thr.start()
	elif var == "h":
		mut_impr.release()
		print '\nEl comando m muestra toda la información de uso de la memoria.\n\nEl comando p muestra la información de cada proceso.\n\nEl comando d despliega el uso total del disco.\n\nEl comando l muestra los logins de sistema.\n\nEl comando c muestra el uso del CPU.\n\nEl comando i muestra las interrupciones del sistema.\n\nEl comando clear limpia la terminal.\n\nEl comando exit finaliza este programa.\n'
		
	elif var == "x":
		global i,j
		i=1
		j=1
		mut_impr.release()

		band = 1	#FINALIZA EL MONITOR
	else:
		print "Invalid command..."
	

#MAIN DEL MONITOR
def shell():
	'''Funciones en Shell'''
	global var, band, mut_impr
	os.system("clear")
	while band == 0:

		menu()
		var = raw_input("user@machine$ ")
		command(var)
		sleep(0.5)

shell()
