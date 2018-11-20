#tarea 2

memoria = []

def AddToMem(proceso, dim):
	global memoria
	elementos = len(memoria)
	limite_mem = elementos + dim
	if limite_mem > 30:
		Defrag(proceso, dim)
	else:
		conta=0
		while conta < dim:
			memoria.append(proceso)
			conta+=1
		print("\n---------------------------MAPEO DE MEMORIA -------------------\n")
		for x in memoria[0:10]:
			print('|'+x+'|', end=" ")
		print("\n")
		for x in memoria[10:20]:
			print('|'+x+'|', end=" ")
		print("\n")
		for x in memoria[20:30]:
			print('|'+x+'|', end=" ")
		print("\n")

def FreeMem(proceso, dim):
	global  memoria
	conta = dim
	while conta > 0:
		index = memoria.index(proceso)
		memoria.remove(proceso)
		memoria.insert(index ,'*')
		conta-=1
	print("\n---------------------------MAPEO DE MEMORIA -------------------\n")
	for x in memoria[0:10]:
		print('|'+x+'|', end=" ")
	print("\n")
	for x in memoria[10:20]:
		print('|'+x+'|', end=" ")
	print("\n")
	for x in memoria[20:30]:
		print('|'+x+'|', end=" ")
	print("\n")

def Defrag(proceso, dim):
	global memoria
	existe_espacio = '*' in memoria
	if existe_espacio:
		print("se requiere compactación de memoria")
		espacio = memoria.count('*')
		if espacio >= dim:
			conta = dim
			while conta > 0:
				index = memoria.index('*')
				memoria.remove('*')
				memoria.insert(index ,proceso)
				conta-=1
			print("\n---------------------------MAPEO DE MEMORIA -------------------\n")
			for x in memoria[0:10]:
				print('|'+x+'|', end=" ")
			print("\n")
			for x in memoria[10:20]:
				print('|'+x+'|', end=" ")
			print("\n")
			for x in memoria[20:30]:
				print('|'+x+'|', end=" ")
			print("\n")
		else:
			print("memoria insuficiente...!")
	else:
		print("No hay memoria disponible")



def opcion(numero):
	global memoria
	if numero == '1':
		proceso = input("Nombre del proceso: ")
		existe= proceso in memoria
		if existe:
			print("Proceso ya en memoria")
		else:
			dim = int(input("ingresa el tamaño de tu proceso: "))
			if dim < 2 or dim > 15:
				print("eeror en la dimencion")
			else:
				AddToMem(proceso,dim)
	elif numero == '2':
		proceso = input("Identificador de el proceso: ")
		existe = proceso in memoria
		if existe:
			dim= memoria.count(proceso)
			FreeMem(proceso, dim)
		else:
			print("proceso inexistente...!")
	else:
		print("opcion no valida")

def control():
	while True:
		print("1 => Nuevo proceso")
		print("2 => Liberar proceso")
		print("0 => salir")
		numero = input("starkiller@winux$: ")
		if numero == '0':
			break
		opcion(numero)

control()