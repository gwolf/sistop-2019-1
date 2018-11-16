#!/usr/bin/python3
#Sanchez Espinosa Andrew Blaise
#Proyecto 3 (micro) Sistema de Archivos.

import os
global nombre

# Esta funcion muestra el contenido de un archivo (lectura)
def mst(cmd):
	nombre = cmd[1]
	try:
		f = open(str(nombre)+'.txt','r')
		print(f.read())
		f.close()
	except IOError:
		print("El archivo no existe")

# Esta funcion crear un archivo y puede escribir en el mismo (crea y puede escribir)
def crr(cmd):
	nombre = cmd[1]
	f= open(str(nombre)+'.txt','w')
	try:	
		f.write(cmd[2])
		f.close()
	except IndexError:
		f.close()

# Esta funcion agraga informacion al archivo (escribe sino existe se crea)
def agg(cmd):
	nombre = cmd[1]
	f = open(str(nombre)+'.txt','a')
	try:	
		f.write(cmd[2])
		f.close()
	except IndexError:
		print("No tiene informacion para agregar")
		f.close()


# Esta funcion borra un archivo (eliminar)
def brr(cmd):
	try:
		os.remove(str(cmd[1])+'.txt')
	except OSError:
		print("El archivo no existe")

# Esta funcion lista el directorio actual
def lsdoc(cmd):
	os.system('dir -B')

# Esta funcion solo imprime en la terminal la ayuda para los comandos a usar
def ayuda(cmd):
	print("\t -- Escriba lsdoc para mostrar los archivos en el directorio ")
	print("\t -- Escriba brr nombreArchivo para borrar ")
	print("\t -- Escriba crr nombreArchivo Contenido para crear un archivo ")
	print("\t -- Escriba mst nombreArchivo para mostrar el contenido de un archivo ")
	print("\t -- Escriba agg nombreArchivo TextoParaAgregar") 
	print("\t       para agregar informacion a un archivo ya creado ")
	print("\t -- Escriba yabasta para cerrar el (micro) Sistema de Archivos ")

# Funcion principal para el manejo del programa Micro Sistema de Archivos BlaiseSe (MSAB) 
def MSAB():
	print("\n\t Bienvenido al (micro) Sistema de Archivos BlaiseSe.")
	print("\t -- Escriba ayuda para ayuda ")

	cmd =raw_input("~$:  ").split(" ")
	lscmd={"lsdoc":lsdoc,"brr":brr,"mst":mst,"ayuda":ayuda,"crr":crr,"agg":agg}
	while cmd[0] != "yabasta":
		try:
			func=lscmd[cmd[0]]
			if len(cmd)>3:	
				aux=""
				for i in range(2,len(cmd)):
					aux+=cmd[i]+" "
				cmd=[cmd[0],cmd[1],aux]
			func(cmd)
		except KeyError:
			print("error 404 -.-' ")
		cmd=raw_input("~$: ").split(" ")

MSAB()
