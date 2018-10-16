# *-* encoding: utf-8 *-*
#!/usr/bin/python
import threading
import commands
import os, sys
import time

semaforo=threading.Semaphore(0) #Se señaliza con un semaforo

def multiProc():
	os.system("clear")

	print "\t\t\t Ejemplo de multiprocesamiento"
	print "\nEste es solo un ejemplo de como crear multiprocesos.\n"
	def worker():
	    print threading.currentThread().getName(), 'Lanzado' #Se crea el hilo y obtiene su nombre
	    time.sleep(5)
	    print threading.currentThread().getName(), 'Deteniendo'
	def servicio():
	    print threading.currentThread().getName(), 'Lanzado'
	    time.sleep(5)
	    print threading.currentThread().getName(), 'Deteniendo'

	t = threading.Thread(target=servicio, name='Servicio')
	w = threading.Thread(target=worker, name='Worker:')
	z = threading.Thread(target=worker)

	w.start()
	time.sleep(3)
	z.start()
	time.sleep(5)
	t.start()

	time.sleep(30)
	semaforo.release()
	return 0

def Processor():
	os.system("clear")

	print "\t\t\t Procesador"
	mod=commands.getoutput("cat /proc/cpuinfo | grep \"model name\"")
	cores=commands.getoutput("cat /proc/cpuinfo | grep \"cpu cores\"")
	bugs=commands.getoutput("cat /proc/cpuinfo | grep \"bugs\"")
	addSize=commands.getoutput("cat /proc/cpuinfo | grep \"address sizes\"")
	mhz=commands.getoutput("cat /proc/cpuinfo | grep \"cpu MHz\"")

	print "Modelo de procesador:\n" + mod + "\n"
	print "Nucleos:\n" + cores + "\n"
	print "Vulnerabilidades:\n" + bugs + "\n"
	print "Tamaño de directorios:\n" + addSize + "\n"
	print "MHz del procesador:\n" + mhz + "\n"

	time.sleep(30)
	semaforo.release()
	return 0

def vmstat():
	os.system("clear")
	var = commands.getoutput('vmstat -s -S M') #Se guarda la cadena de version en 'var' 
	print var #Impresión de 'ver' para mostrar la version del sistema 
	#print "\n\n\nPresione ctrl+c para regresar al menu\n"
	time.sleep(20)
	semaforo.release() #Libera al hilo opcion para regresar al hilo menu
	return 0

def Utime():
	os.system("clear")
	print " Fecha---Tiempo en uso"
	tTotal = commands.getoutput('uptime -s -S M') 
	print tTotal
	time.sleep(20)
	semaforo.release() #Libera al hilo opcion para regresar al hilo menu
	return 0

def Interrupc():
	os.system("clear")
	print " Interrupciones"
	inter = commands.getoutput('interrupts -s -S M') 
	print inter
	time.sleep(20)
	semaforo.release() #Libera al hilo opcion para regresar al hilo menu
	return 0

def Menu():
	global semaforo
	opt='0'

	while opt != '6':
		os.system("clear")
		op={'1':multiProc, '2':Processor, '3':vmstat, '4':Utime, '5':Interrupc}

		print "\t\t\t\t Monitor de Recursos\n\n"
		print "\t1. Ejemplo de multiprocesamiento.\n"
		print "\t2. Caracteristicas del procesador.\n"
		print "\t3. Reporte de Memoria Virtual\n"
		print "\t4. Tiempo encendido.\n"
		print "\t5. Interrupciones.\n"
		print "\t6. Salir\n"
		opt=raw_input( "\n\t>> ")
		try:
			res=op[opt]()
			semaforo.acquire()
		except:
			if opt != '6':
				print "Opcion invalida"
Menu()