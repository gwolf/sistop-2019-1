import os #Solo para limpiar la terminal.

memoria = []

"""La función 'fillMem' se usa para agregar nuevos procesos a la memoria, se verifica que haya espacio libre y en caso de no tener 
espacio para agregar más elementos se llama a la función 'compact'. Al agregar nuevos procesos se muestra el mapa de memoria"""

def fillMem(proc, tam):
	global memoria

	elem = len(memoria)
	limMem = elem + tam
	if limMem > 30:
		compact(proc, tam)
	else:
		i=0
		while i < tam:
			memoria.append(proc)
			i+=1
		os.system("cls")
		imprimeMapa()
		print("\n")

"""La función 'eraseMem' se usa para eliminar elementos de la memoria, se verifica que exista el proceso indicado y de ser asi se elimina.
Una vez eliminado el elemento se muestra el mapa de memoria."""

def eraseMem(proc, tam):
	global memoria

	i = tam
	while i > 0:
		index = memoria.index(proc)
		memoria.remove(proc)
		memoria.insert(index, '-')
		i-=1
	os.system("cls")
	imprimeMapa()
	print("\n")

"""La función 'compact' sirve para agregar procesos a la memoria, sólo si existen suficientes '-' en donde se puedan remplazar por el 
proceso que se quiere ingresar. De ser posible agregar nuevos elementos, muestra el mapa de memoria."""

def compact(proc, tam):
	global memoria

	espExist = '-' in memoria[0:30] #Aquí no sé si es correcto en como hago el barrido para hacer la compresión.
	if espExist:
		print("Se requiere compactación de memoria")
		espacio = memoria.count('-')
		if espacio >= tam:
			i = tam
			while i > 0:
				index = memoria.index('-')
				memoria.remove('-')
				memoria.insert(index, proc)
				i-=1
			os.system("cls")
			imprimeMapa()
			print("\n")
		else:
			os.system("cls")
			print("Memoria insuficiente.")
	else:
		os.system("cls")
		print("No hay memoria disponible.")

#La función "opcion" sirve para mostrar las opciones que el usuario puede escoger, además de verificar si los procesos que se quieren agregar ya existen.

def opcion(num):
	global memoria

	if num == '1':
		proc = input("Ingresa el nombre del proceso: ")
		existe = proc in memoria
		if existe:
			print("El proceso ya existe en memoria.")
		else:
			tam = int(input("Ingresa el tamaño del proceso: "))
			if tam < 2 or tam > 15:
				print("Tamaño de proceso inválido.")
			else:
				fillMem(proc, tam)
	elif num == '2':
		proc = input("Ingresa el nombre del proceso: ")
		existe = proc in memoria
		if existe:
			tam = memoria.count(proc)
			eraseMem(proc, tam)
		else:
			print("No existe el proceso.")
	else:
		print("Opción inválida.")

def control():
	while True:
		print("1. Agregar proceso")
		print("2. Quitar proceso")
		print("0. Salir")
		num = input(">> ")
		if num == '0':
			break
		opcion(num)

def imprimeMapa():
	global memoria

	print("\n───────────────── MEMORY MAP ─────────────────\n")
	for x in memoria[0:10]:
		print(' ' + x + ' ', end=" ")
	print("\n")
	for x in memoria[10:20]:
		print(' ' + x + ' ', end=" ")
	print("\n")
	for x in memoria[20:30]:
		print(' ' + x + ' ', end=" ")

control()