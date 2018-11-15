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

def crear(nombre):
	if not existeArchivo():
		nombre=nombre+'\n'
		posicion=posicion_archivos()-1
		print ("Ingresa el contenido del archivo:\n")
		cadena = raw_input()
		cadena = completa_cadena(cadena,nombre)
		with open('hi','r+') as arch:
			archComoLista=arch.read().splitlines()
			archComoLista.insert(posicion_archivos(),nombre)
			archComoLista.append(cadena)
			f.writelines("\n".join(archComoLista))
		listaPrincipal.append(nombre)
	else:
		print("Archivo ya existe!")
	return listaPrincipal

def posicion_archivos():
	posicion = 0
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion=archComoLista.index("--%%Contenidos%%--")
	return posicion

def completa_cadena(cadena,nombre):
	cadena = '--%%Contenidos%%--' + nombre + '\n' + cadena + '\n--%%Contenidos%%--' + nombre
	return cadena

def modificar(nombre):
	print ("Ingresa el contenido del archivo:\n")
	cadena = raw_input()
	with open('hi','r+') as arch:
		archComoLista=arch.read().splitlines()
		archComoLista.insert(final_cont()-1,cadena)
		f.writelines("\n".join(archComoLista))

def final_cont():
	posicion=0
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion = archComoLista.index("--%%Contenidos%%--" + nombre)
	return posicion

def leer(nombre):
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
		posicion=archComoLista.index("--%%Contenidos%%--" + nombre)
	return posicion

def borrar(nombre):
	with open('hi','r+') as arch:
		archComoLista=arch.read().splitlines()
		archComoLista.remove(nombre)
		del archComoLista[posicion_inicial_cont(nombre),final_cont(nombre)]
		f.writelines("\n".join(archComoLista))

def leer_todo():
	f = open('hi','r')
	for line in f:
		print line

def limite_de_Archivos():
	with open('hi','r') as arch:
		archComoLista=arch.read().splitlines()
		posicion=archComoLista.index("--%%Contenidos%%--")
	return posicion

def limite_de_Contenidos(indice):
	limites=[]
	with open ('hi','r') as lineas:
		for linea in lineas:
			limiteInferior+=1
			if linea == '$$&&//((conFin': break
	return limiteInferior

def menu():
	creaContenedor('Hi')
	salir = True
	while salir:
		print("\n")
		print("Listar el directorio     ->   listar\n")
		print("Agregar Archivo          ->   crear nombre\n")
		print("Modificar Archivo        ->   mod nombre\n")
		print("Leer Archivo             ->   leer nombre\n")
		print("Borrar Archivo           ->   borrar nombre\n")
		print("Salir                    ->   salir")
		opc = raw_input("\n>>")
		#leer_todo()
		if opc == 'salir':
			salir = False
		elif opc == 'listar' :
			listar()
		elif opc == 'crear' :
			crear(nombre)
		elif opc == 'mod' :
			modificar(nombre)
		elif opc == 'borrar' :
			borrar(nombre)
		else:
			error()

menu()





