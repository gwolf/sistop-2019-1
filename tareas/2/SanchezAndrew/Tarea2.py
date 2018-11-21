#!/usr/bin/python3
#Sanchez Espinosa Andrew Blaise.

memoria = []

# Para verificar si hay espacio libre en la memoria, cuando no hay espacio libre se hace 
# la compactacion
def llena_memoria(proceso, tamano):
	global memoria
	elementos = len(memoria)
	limite_mem = elementos + tamano
	if limite_mem > 30:
		compactacion(proceso, tamano)
	else:
		conta=0
		while conta < tamano:
			memoria.append(proceso)
			conta+=1
		print("\n================= MAPA DE MEMORIA =================\n")
		for x in memoria[0:10]:
			print('|'+x+'|')
		#print(" ")
		for x in memoria[10:20]:
			print('|'+x+'|')
		#print(" ")
		for x in memoria[20:30]:
			print('|'+x+'|')
		#print(" ")


# Para eliminar el proceso seleccionado y mostrar un asterisco en su lugar
def vacia_memoria(proceso, tamano):
	global  memoria
	conta = tamano
	while conta > 0:
		index = memoria.index(proceso)
		memoria.remove(proceso)
		memoria.insert(index ,'*')
		conta-=1
	print("\n================= MAPA DE MEMORIA =================\n")
	for x in memoria[0:10]:
		print('|'+x+'|')
	print(" ")
	for x in memoria[10:20]:
		print('|'+x+'|')
	#print(" ")
	for x in memoria[20:30]:
		print('|'+x+'|')
	#print(" ")

#Para realizar la compactacion en la memoria
def compactacion(proceso, tamano):
	global memoria
	existe_espacio = '*' in memoria
	if existe_espacio:
		print("se requiere compactacion de memoria")
		espacio = memoria.count('*')
		if espacio >= tamano:
			conta = tamano
			while conta > 0:
				index = memoria.index('*')
				memoria.remove('*')
				memoria.insert(index ,proceso)
				conta-=1
			print("\n================= MAPA DE MEMORIA =================\n")
			for x in memoria[0:10]:
				print('|'+x+'|')
			#print(" ")
			for x in memoria[10:20]:
				print('|'+x+'|')
			#print(" ")
			for x in memoria[20:30]:
				print('|'+x+'|')
			#print(" ")
		else:
			print("memoria insuficiente...!")
	else:
		print("No hay memoria disponible")


#Para saber el proceso a agregar y el tamano 
def opcion(numero):
	global memoria
	if numero == '1':
		proceso = raw_input("ingresa el nombre del proceso: ")
		existe= proceso in memoria
		if existe:
			print("El proceso ya existe en memoria..!")
		else:
			tamano = int(input("ingresa el tamano de tu proceso: "))
			if tamano < 2 or tamano > 15:
				print("tamano de proceso: invalido...!")
			else:
				llena_memoria(proceso,tamano)
	elif numero == '2':
		proceso = raw_input("ingresa el nombre del proceso: ")
		existe = proceso in memoria
		if existe:
			tamano= memoria.count(proceso)
			vacia_memoria(proceso, tamano)
		else:
			print("proceso inexistente...!")
	else:
		print("opcion invalida..!")

# Esta funcion es para mostrar las opciones y obtener la opcion a seleccionar
def control():
	while True:
		print("1 => Agregar proceso")
		print("2 => Quitar proceso")
		print("0 => salir")
		#print("$$ ")
		numero = raw_input("$$ ")
		if numero == '0':
			break
		opcion(numero)

control()

