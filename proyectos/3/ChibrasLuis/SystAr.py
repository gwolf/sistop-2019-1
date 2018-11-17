# Nota: Solo permite crear archivos, directorios y manipular los mismos si su nombres son de máximo 8 caracteres

import os

def main():
	print ("\t\t\t!!!Bienvenido al micro sistema!!!\n Los comandos son: nDir, nArch, lista, dDir, dArch, edit, mues, entra, limpia, manual\n\t\t\t(para mas información consulte manual) \n")
	while 1:
		comando = input("**> ")
		comandos(comando)
		
def comandos(opcion): # Valida que se ingresen solo los comandos aceptados
	if opcion == 'nDir':
		nDir(limite(input("¿Como se llamara el nuevo directorio?: ")))
		
	elif opcion == 'nArch':
		nArch(limite(input("¿Como se llamara el nuevo archivo?: ")))

	elif opcion == 'lista':
		lista()

	elif opcion == 'dDir':
		dDir(limite(input("Ingrese el nombre del directorio a eliminar: ")))

	elif opcion == 'dArch':
		dArch(limite(input("Ingrese el nombre del archivo a eliminar: ")))

	elif opcion == 'edit':
		edit(limite(input("Ingrese el nombre del archivo a editar: ")))

	elif opcion == 'mues':
		mues(limite(input("Ingrese el nombre del archivo a mostrar: ")))

	elif opcion == 'entra':
		entra(input("Ingrese la ruta al directorio: "))

	elif opcion == 'limpia':
		limpia()

	elif opcion == 'manual':
		manual()

	else:
		print("Ingrese un comando valido:\nnDir, nArch, lista, dDir, dArch, edit, mues, manual")


def limite(com):# Impone una restricción de máximo 8 caracteres a los argumentos 
	if len(com) > 8:
		print("Los argumentos deben ser menores a 9 caracteres")
		main()
	else:
		return com

def nDir(com):# Crea nuevo directorio
	os.system("mkdir " +com)

def nArch(com): # Crea un nuevo archivo 
	os.system("touch "+ com)

def lista():# Lista el contenido del directorio actual 
	os.system("ls")

def dDir(com):
	os.system("rm -r "+com)

def dArch(com):# Elimina un archivo
	os.system("rm "+ com)

def edit(com):# Edita un archivo
	os.system("vi "+ com)

def mues(com):# Muestra el contenido de un archivo
	os.system("cat "+ com)

def entra(com):
	os.chdir(com)

def limpia():
	os.system("clear")

def manual(): # Despliega una breve explicación de los comandos
	print("nDir: Permite crear un nuevo directorio en el directorio actual\nnArch: Crea un nuevo archivo en el directorio actual\nlista: Imprime en pantalla el contenido del directorio actual\ndDir: Elimina el directorio seleccionado\ndArch: Elimina el archivo seleccionado\nedit: Lanza el editor Vi en el cual es posible editarel contenido del archivo seleccionado\nmues: Presenta el contenido del archivo seleccionado\nentra: Permite acceder a otros directorios ingresando la ruta Eje ' Documento/Luis' o regresar al directorio padre Eje ' . . '\nlimpia: borra los datos en pantalla  ")


main()