# -*- coding: utf-8 -*-
import os
import itertools
from time import sleep

contadorArchivo = 0

def existeArchivo(nombre):
	return os.path.isfile(nombre)

def creaContenedor(nombre):
	if existeArchivo(nombre):
		archivo = open(nombre,'r')
		archivo.close()
	else:
		print ("No se encontro el archivo base, creando...")
		archivo = open(nombre,'w')
		listaDeArchivos=("\n--%%Contenidos%%--")
		archivo.write(listaDeArchivos)
		archivo.close()

def error():
	print ("Error, regresando al menu...")
	sleep(4)
	return menu()

def listar():
	with open ('hi','r') as arch:
		for line in range(limite_de_Archivos()):
			print line

def crear():
	print ("Ingresa el nombre del archivo a crear:\n>>")
	nombre=raw_input()
	if not existeArchivo(nombre):
		print ("Ingresa el contenido del archivo:\n")
		cadena = raw_input()
		cadena = completa_cadena(cadena,nombre)
		nombre=nombre+'\n'
		with open('hi','r+') as arch:
			archComoLista=arch.read().splitlines()
			archComoLista.insert(0,nombre)
			archComoLista.append(cadena)
			arch.writelines("\n".join(archComoLista))
	else:
		print("Archivo ya existe!")

def completa_cadena(cadena,nombre):
	cadena = '--%%Contenidos%%--I' + nombre + '\n' + cadena + '\n--%%Contenidos%%--F' + nombre
	return cadena

def modificar():
	print ("Ingresa el nombre del archivo a modificar(Solo agregar contenido):\n")
	nombre=raw_input()
	if existeArchivo(nombre):	
		print ("Ingresa el contenido del archivo:\n")
		cadena = raw_input()
		with open('hi','r+') as arch:
			archComoLista=arch.read().splitlines()
			archComoLista.insert(final_cont(nombre)-1,cadena)
			arch.writelines("\n".join(archComoLista))
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
	print ("Ingresa el nombre del archivo a leer:\n>>")
	nombre=raw_input()
	if existeArchivo(nombre):
		with open ('hi','r') as arch:
			arch.seek(posicion_inicial_cont(nombre))
			for line in range(tamaio_contenido(nombre)):
				print line
	else:
		print ("No existe el archivo...")

def posicion_inicial_cont(nombre):
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion=archComoLista.index("--%%Contenidos%%--I" + nombre)
	return posicion

def borrar():
	print ("Ingresa el nombre del archivo a borrar:\n>>")
	nombre=raw_input()
	if existeArchivo(nombre):
		with open('hi','r+') as arch:
			archComoLista=arch.read().splitlines()
			archComoLista.remove(nombre)
			del archComoLista[posicion_inicial_cont(nombre),final_cont(nombre)]
			arch.writelines("\n".join(archComoLista))
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
	creaContenedor('Hi')
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
		leer_todo()
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





