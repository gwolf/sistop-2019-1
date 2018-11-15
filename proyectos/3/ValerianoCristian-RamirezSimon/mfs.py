import os
from time import sleep

conIni="$$&&//((conIni"
conFin="$$&&//((conFin"
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
		listaDeArchivos=("$$&&//((arIni\n\n$$&&//((carFin")
		archivo.write(listaDeArchivos)
		archivo.close()

def error():
	print ("Error, regresando al menu...")
	sleep(4)
	return menu()

def listar():
	print ("listar()")

def crear():
	print ("c")

def modificar():
	print ("m")

def leer():
	print ("le")

def borrar():
	print ("b")

def leer_todo():
	f = open('hi','r')
	for line in f:
		print line

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
		else:
			error()

menu()





