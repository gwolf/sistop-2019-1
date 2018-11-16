#a qui creamos las acciones de nuestro sistema de archivos
from Pila import Pila
from Archivo import Archivo
import pickle
#Aqui se definen las pilas como centros de almacenamiento
p= Pila()
p2= Pila()
pa= Pila()
pa2= Pila()
#Se crean las acciones de nuestros sistemas de archivos
#Nota se almacenan los valores con la funcion push y se eliminan con la pop
#ademas se obtiene el valor con la funcion top
class FileSystem: 
	def Crear(self):
		nomb=raw_input("Ingrese nombre del archivo:\n")
		read = raw_input("Ingrese contenido:\n")
		ar=Archivo()
		pa.push(ar.write(read))
		p.push(nomb)
	def Elimin(self):
		nomb=raw_input("Ingrese nombre del archivo:\n")
		if p.vacia():
			print("No existe su archivo");
		i=0
		j=0
		while i<p.tam():
			if nomb==p.top():
				p.pop()
				pa.pop()
				
				print("se ha eliminado el archivo"+nomb)
				break
			else:
				p2.push(p.top())
				pa2.push(pa.top())
				p.pop()
				pa.pop()
				i=i+1
		while j<p2.tam():
			p.push(p2.top())
			pa.push(pa2.top())
			pa2.pop()
			p2.pop()
			i=i+1
	def Busc(self):
		nomb=raw_input("Ingrese nombre del archivo:\n")
		if p.vacia():
			print("No existe su archivo");
		i=0
		j=0
		while i<p.tam():
			if nomb==p.top():
				print("se ha encontrado el archivo"+nomb)
				break
			else:
				p2.push(p.top())
				p.pop()
				i=i+1
		while j<p2.tam():
			p.push(p2.top())
			p2.pop()
			i=i+1
	def Mostrar(self):
		i=0
		j=0
		while i<p.tam():
			print(p.top())
			p2.push(p.top())
			p.pop()
			i=i+1
		while j<p2.tam():
			p.push(p2.top())
			p2.pop()
			i=i+1
	def Leer(self):
		nomb=raw_input("Ingrese nombre del archivo:\n")
		if p.vacia():
			print("No existe su archivo");
		i=0
		j=0
		while i<p.tam():
			if nomb==p.top():
				print ("NOMBRE DEL ARCHIVO:\n"+nomb+"\n")
				print (pa.top())
				break
			else:
				p2.push(p.top())
				pa2.push(pa.top())
				pa.pop()
				p.pop()
				i=i+1
		while i<p2.tam():
			p.push(p2.top())
			pa.push(pa2.top())
			pa2.pop()
			p2.pop()
			i=i+1
	def Persistir(self):
        	filename=raw_input("Archivo para persistir:\n")
       		f = open(filename, 'wb')
        	pickle.dump([p, p2, pa, pa2], f)
        	print "Sistema volcado en ", filename, "\n"

	def Recuperar(self):
        	filename2=raw_input("Archivo para recuperar:\n")
        	f = open(filename2, 'rb')
        	temp = pickle.load(f)
        	print "Recuperado: ", temp
        	p=temp[0]
        	p2=temp[1]
        	pa=temp[2]
        	pa2=temp[3]
        	print "Sistema leido de ", filename2, "\n"
        	self.Mostrar()



		

