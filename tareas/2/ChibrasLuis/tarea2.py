#primer ajuste
# Nota no funciona del todo bien a veces no se ejecuta a la primera y nunca logre que metiera los procesos de corrido (no supe como manipular los índices del ciclo for)
import random


memoria = []

def main():

	ent=input("Asignar (0) o liberar (1): ")


def menu(opcion):
	if opcion == '0':
		Asignar()
	elif opcion == '1':
		Borrar()
	else:
		print("ingrese una opcion valida")
	

def Consecutivos():# Calcula los espacios consecutivos vacíos en el arreglo
	global memoria
	consecutivo=0
	anterior=0
	for i in memoria:
		if i == '-':
			consecutivo=consecutivo+1
			if anterior<consecutivo:
				anterior=consecutivo
		else:
			consecutivo=0

	return anterior

def llenado(): # llena de manera aleatoria el arreglo
	global memoria
	ar = 30
	Op=['A','B','C','D','-']
	while ar !=0:
		res=random.choice(Op)
		memoria.append(res)
		if random.choice(Op)!= res:
			ar=ar-1
			memoria.append(res)
		ar=ar-1

def Compactacion():
	#print (memoria.count('-'))
	memoria.sort(key=None,  reverse=True)


def Asignar():
	pro=input("Ingrese Nombre del Proceso (A-Z): ")
	tam=input("Ingrese le tamano de (" + pro + "): ")
	tam=int(tam)
	libre=int(Libres())

	if tam > libre:
		print ("Espacio insuficiente elimine un proceso para continuar")
	elif Consecutivos() < tam:
		print("compactacion requerida")
		Compactacion()
		ReAsignando(pro, tam)

	else:
		ReAsignando(pro, tam)
		
def ReAsignando(A, B):# B es tamano del proceso A nombre del proceso
	global memoria
	cont=0
	cont2=B
	for i in (memoria):
			if i == '-' and cont2 > 0 :
				posi=Disponible(B)
				memoria.remove('-')
				memoria.insert(posi, A)
				cont=cont+1
				cont2=cont2-1

	Muestra()

def Disponible(C): # intenta encontrar un espacio vacío lo suficientemente mente grande para alojar el proceso 
	global memoria
	consecutivo=0
	anterior=0
	ind=0
	for i in memoria:
		if i == '-':
			consecutivo=consecutivo+1
			if anterior<consecutivo:
				anterior=consecutivo
				if C == consecutivo:
					ind=memoria.index('-')
					#ind=ind-C
					print(ind)
					return ind

		else:
			consecutivo=0

def Borrar(): 
	global memoria
	eli=input("Que proceso desea eliminar: ")
	for i in memoria:
		if i == eli:
			posi= memoria.index(eli)
			memoria.remove(eli)
			memoria.insert( posi,'-')	
	Muestra()

def Libres():
	cont=0
	for i in memoria:
		if i == '-':
			cont=cont+1
	return cont

def Muestra():
	global memoria
	presenta=''.join(memoria)
	print (presenta)

def main():
	
	llenado()
	while True:
		Muestra()
		ent=input("Asignar (0) o liberar (1): ")
		menu(ent)

main()
