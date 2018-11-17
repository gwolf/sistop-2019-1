#!/usr/bin/python3

import wx
import threading
import time
import os

OpSelec = {'Disco':True, 'Memoria':True, 'Procesos':True, 'Cpu':True, 'MarcaParaSeleccionar':True, 'Tem':True}


mutex = threading.Semaphore(1)
thr = 0


class OpcionesM(wx.Frame):
# Todas estas secuencias son para iniciar la ventana donde apareceran las opciones a seleccionar#
  def __init__(self, parent, id, title):
	#creacion de una ventana de tamaño 300,170
    wx.Frame.__init__(self, parent, id, title, size=(300, 170))

	#Se declara un panel con la biblioteca wxpython
    Opciones = wx.Panel(self, -1)

##Comienza creacion de casillas
	#Creacio de casillas con el metodo CheckBox de biblioteca wx
	#El metodo SetValue es para saber si esta o no seleccionada la casilla (por default las activo)
	#El metodo EVT_CHECKBOX es para saber si marcan o desmarcan una casilla
    self.cb = wx.CheckBox(Opciones, -1, 'Disco', (10, 10))
    self.cb.SetValue(True)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolDisk)

    self.cb = wx.CheckBox(Opciones, -1, 'Memoria', (120, 10))
    self.cb.SetValue(True)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolMemory)
    
    self.cb = wx.CheckBox(Opciones, -1, 'Procesos', (10, 45))
    self.cb.SetValue(True)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolProcess)
    
    self.cb = wx.CheckBox(Opciones, -1, 'Cpu', (120, 45))
    self.cb.SetValue(True)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolCpu)

    self.cb = wx.CheckBox(Opciones, -1, 'Tem', (10, 80))
    self.cb.SetValue(True)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolTem)


    self.cb = wx.CheckBox(Opciones, -1, '', (350, 80))
    self.cb.SetValue(True)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolSelec)

##Termina creacion de casillas

##Comienza creacion de botones
	#Agrego botones para hacer mas amigable la interaccion
	#Se crean con el metodo wx.Button(dondeBuscar,ValorDefinido(-1), tamano(x,y), posicion(x,y))
	#El metodo EVT_BUTTON sirve para saber cuando se da click en el boton
    self.botonLimpiar = wx.Button(Opciones, -1, 'Borrar', size=(60,30), pos=(10,130))
    self.Bind(wx.EVT_BUTTON, self.Limpiar, self.botonLimpiar)

    self.botonAceptar = wx.Button(Opciones, -1, 'Aceptar', size=(70,30), pos=(120,130))
    self.Bind(wx.EVT_BUTTON, self.Aceptar, self.botonAceptar)
##Termina creacion de botones
	
	#para mostrar la ventana (Show()) y centrarla (Centre())
    self.Show()
    self.Centre()

# En la seccion siguiente se puede saber que opcion es seleccionada y mostrarla en la terminal del sistema #
	#Definisiones para saber que casilla se selecciona
  def boolSelec(self, event):
    global marcaSelec
    if self.cb.GetValue():
      marcaSelec = not marcaSelec
      OpSelec["MarcaParaSeleccionar"] = marcaSelec
      print marcaSelec

  def boolCpu(self, event):
    global marcaCPU
    if self.cb.GetValue():
      marcaCPU = not marcaCPU
      OpSelec["Cpu"] = marcaCPU
      print marcaCPU

  def boolTem(self, event): 
    global marcaTem
    if self.cb.GetValue():
      marcaTem = not marcaTem
      OpSelec["Tem"] = marcaTem
      print marcaTem

  def boolProcess(self, event):
    global marcaProcesos
    if self.cb.GetValue():
      marcaProcesos = not marcaProcesos
      OpSelec["Procesos"] = marcaProcesos
      print marcaProcesos


  def boolDisk(self, event):
    global marcaDisco
    if self.cb.GetValue():
      marcaDisco = not marcaDisco
      OpSelec["Disco"] = marcaDisco
      print marcaDisco
            
  def boolMemory(self, event):
    global marcaMemoria
    if self.cb.GetValue():
      marcaMemoria = not marcaMemoria
      OpSelec["Memoria"] = marcaMemoria
      print marcaMemoria    
	
	#estas son de los botones pero tienen la misma funcion que las de las casillas
  def Limpiar(self,event):
    global mutex
    mutex.acquire()
    os.system("clear")
    mutex.release()

  def Aceptar(self,event):
    hilo(OpSelec)


#Estas variables se hacen globales en las definiciones para
# poder hacer uso de ellas como en este caso para saber si son seleccionadas o no
marcaTem = True
marcaDisco = True
marcaMemoria = True
marcaProcesos = True
marcaCPU = True
marcaSelec = True


## >>>>>> Definiciones para mostrar en la terminal
##### >>>>>>> la informacion de las opciones seleccionadas



	#informacion del dico duro
def Disk():
  global mutex
  mutex.acquire()
  print ">>>Disco duro\n"
  os.system("cd")
  os.system("du") #Descubre archivos mas grandes del sistema
 mutex.release()
  
	#informacion de la memoria
def Mem():
  global mutex
  mutex.acquire()
  print ">>>Memoria\n"
  os.system("free")
  os.system("cat /proc/meminfo") #Verificar el uso de memoria
  mutex.release()

	#informacio de los procesos
def Proc():
  global mutex
  mutex.acquire()
  print ">>>Procesos\n"
  os.system("ps")     #Procesos actuales
  os.system("pstree") #para imprimir los procesos en forma de arbol (mejora la presentacion)
  mutex.release()
  
 	#informacion del cpu
def CPU():
  global mutex
  mutex.acquire()
  print ">>> Informacion del CPU\n"
  os.system("cat /proc/cpuinfo")
  mutex.release()

def Tem():
  global mutex
  mutex.acquire()
  print ">>> Temperatura del CPU\n"
  os.system(" sensors ")
  mutex.release()

##Terminan las definiciones para mostrar la informacion requerida

##Esta definicion solo busca la opcion a monitorear
	#Para elgir la Opcion a monitorear
def Opciones(opcion):

  global hilo
  global thr
  if (opcion == "Disco"):
    filament = threading.Thread(target = Disk)
    filament.start()
  elif (opcion == "Memoria"):
    filament = threading.Thread(target = Mem)
    filament.start()
  elif (opcion == "Procesos"):
    filament = threading.Thread(target = Proc)
    filament.start()
  elif (opcion == "Cpu"):
    filament = threading.Thread(target = CPU)
    filament.start()
  elif (opcion == "Tem"):
    filament = threading.Thread(target = Tem)
    filament.start()
  else:
   print "Intente de nuevo"

##Fin de la definicion



##Inicia el lanzador de Hilos
def hilo(OpSelec):
  if OpSelec["Disco"] == True:
    filament0 = threading.Thread(target = Disk)
    filament0.start()
  if OpSelec["Memoria"] == True:
    filament1 = threading.Thread(target = Mem)
    filament1.start()
  if OpSelec["Procesos"] == True:
    filament2 = threading.Thread(target = Proc)
    filament2.start()
  if OpSelec["Cpu"] == True:
    filament3 = threading.Thread(target = CPU)
    filament3.start()
  if OpSelec["Tem"] == True:
    filament4 = threading.Thread(target = Tem)
    filament4.start()

##Fin del lanzador de Hilos


##Esta definicion fue desactivada para poder manejar la ventana
def MS():	#MonitorSistema
  global opcion, thr, mutex
  os.system("clear")
  while thr == 0:
      time.sleep(1)
      print "===>Opciones<===\n"
      print "disco\tmemoria\tprocesos\tcpu\tcpuTemp"
      opcion = raw_input("ingreseOpcion\t\t")
      Opciones(opcion)
  mutex.release()

#MS()		#MonitorSistema
# Estos se ocupan para hacer uso de la ventana con wxpython #
casillasBooleanas = wx.App()
OpcionesM(None, -1, 'Opcion a monitorear')
casillasBooleanas.MainLoop()
#Sanchez Espinosa Andrew Blaise

