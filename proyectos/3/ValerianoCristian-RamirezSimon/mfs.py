# -*- coding: utf-8 -*-
import os
import itertools
from time import sleep

contadorArchivo = 0

def existeArchivo(nombre):
	return os.path.isfile(nombre)

def existe_archivo_interno(nombre):
	interno=0
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		for line in archComoLista:
			#print ("Dentro de interno:"),line,nombre
			if line == nombre:
				interno = True
	return interno			

def creaContenedor(nombre):
	if existeArchivo(nombre):
		archivo = open(nombre,'r')
		archivo.close()
	else:
		print ("No se encontro el archivo base, creando...")
		archivo = open(nombre,'w')
		listaDeArchivos=("--%%ContenidosArchivos%%--")
		archivo.write(listaDeArchivos)
		archivo.close()

def error():
	print ("Error, regresando al menu...")
	sleep(3)
	return menu()

def listar():
	with open ('hi','r') as arch:
		for line in arch:
			if line == "--%%ContenidosArchivos%%--":
				break
			else:
				print line

def crear():
	print ("Ingresa el nombre del archivo a crear:\n")
	nombre=raw_input(">>")
	if not existe_archivo_interno(nombre):
		print ("Ingresa el contenido del archivo:\n")
		cadena = raw_input()
		with open('hi','r+') as arch:
			archComoLista=arch.read().splitlines()
			#print archComoLista
			archComoLista.insert(0,"\n"+nombre+"\n")
			cadena = completa_cadena(cadena,nombre)
			archComoLista.append(cadena)
			archComoLista.insert(0,'\n')
			#print archComoLista
			arch.writelines(archComoLista)
	else:
		print("Archivo ya existe!")

def completa_cadena(cadena,nombre):
	cadena = "\n--%%Contenidos%%--I" + nombre + "\n" + cadena + "\n--%%Contenidos%%--F" + nombre
	return cadena

def modificar():
	print ("Ingresa el nombre del archivo a modificar(Solo agregar contenido):\n")
	nombre=raw_input(">>")
	#print nombre, existe_archivo_interno(nombre)
	if existe_archivo_interno(nombre):	
		print ("Ingresa el contenido del archivo:\n")
		cadena = raw_input()
		with open('hi','r+') as arch:
			archComoLista=arch.read().splitlines()
			archComoLista.insert(final_cont(nombre)-1,cadena)
			arch.writelines(archComoLista)
	else:
		print ("No existe el archivo...")
		sleep(2)

def final_cont(nombre):
	posicion=0
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion = archComoLista.index("--%%Contenidos%%--F" + nombre)
	return posicion

def leer():
	print ("Ingresa el nombre del archivo a leer:")
	nombre=raw_input(">>")
	if existe_archivo_interno(nombre):
		with open ('hi','r') as arch:
			arch.seek(posicion_inicial_cont(nombre))
			rango=posicion_final_cont(nombre)-posicion_inicial_cont(nombre)
			for line in range(rango):
				print arch.readline()
	sleep(3)

	else:
		print ("No existe el archivo...")
		sleep(2)

def posicion_inicial_cont(nombre):
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion=archComoLista.index("--%%Contenidos%%--I" + nombre)
	return posicion

def posicion_final_cont(nombre):
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion=archComoLista.index("--%%Contenidos%%--F" + nombre)
	return posicion

def borrar():
	print ("Ingresa el nombre del archivo a borrar:\n")
	nombre=raw_input(">>")
	if existe_archivo_interno(nombre):
		with open('hi','r+') as arch:
			archComoLista=arch.read().splitlines()
			archComoLista.remove(nombre)
			#print len(archComoLista),posicion_inicial_cont(nombre),posicion_final_cont(nombre)-1
			for i in range(posicion_final_cont(nombre)-1,posicion_inicial_cont(nombre)):
				archComoLista.pop(i)
			arch.writelines(archComoLista)
	else:
		print ("No existe el archivo")
		sleep(2)

def leer_todo():
	f = open('hi','r')
	for line in f:
		print line

def limite_de_Archivos():
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion=archComoLista.index("--%%Contenidos%%--")
	return posicion

def menu():
	creaContenedor('hi')
	salir = True
	while salir:
		print("\n")
		print("Listar el directorio     ->   listar\n")
		print("Crear Archivo            ->   crear\n")
		print("Modificar Archivo        ->   mod\n")
		print("Leer Archivo             ->   leer\n")
		print("Borrar Archivo           ->   borrar\n")
		print("Salir                    ->   salir")
		opc = raw_input("\n>>")
		#leer_todo()
		if opc == 'salir':
			salir = False
		elif opc == 'listar' :
			listar()
		elif opc == 'crear' :
			crear()
		elif opc == 'mod' :
			modificar()
		elif opc == 'borrar' :
			borrar()
		elif opc == 'leer' :
			leer()
		else:
			error()

menu()




