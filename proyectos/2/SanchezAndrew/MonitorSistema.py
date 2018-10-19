#!/usr/bin/python

import wx
import threading
import time
import os


mutex = threading.Semaphore(1)
thr = 0

class Opciones(wx.Frame):
# Todas estas secuencias son para iniciar la ventana donde apareceran las opciones a seleccionar#
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, size=(300, 170))

    Opciones = wx.Panel(self, -1)

    self.cb = wx.CheckBox(Opciones, -1, 'DISCO', (10, 10))
    self.cb.SetValue(False)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolDisk)

    self.cb = wx.CheckBox(Opciones, -1, 'MEMORIA', (120, 10))
    self.cb.SetValue(False)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolMemory)
    
    self.cb = wx.CheckBox(Opciones, -1, 'PROCESOS', (10, 45))
    self.cb.SetValue(False)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolProcess)
    
    self.cb = wx.CheckBox(Opciones, -1, 'CPU', (120, 45))
    self.cb.SetValue(False)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolCpu)

    self.cb = wx.CheckBox(Opciones, -1, 'MarcaParaSeleccionar', (80, 80))
    self.cb.SetValue(False)
    wx.EVT_CHECKBOX(self, self.cb.GetId(), self.boolAux)

    self.Show()
    self.Centre()

# En la seccion siguiente se puede saber que opcion es seleccionada y mostrarla en la terminal del sistema #

  def boolAux(self, event):
    if self.cb.GetValue():
      print "marcar para seleccionar"

  def boolCpu(self, event):
    if self.cb.GetValue():
      print "CPU"

  def boolProcess(self, event):
    if self.cb.GetValue():
      print "PROCESOS"
      
  def boolDisk(self, event):
    if self.cb.GetValue():
      print "DISCO"
      
  def boolMemory(self, event):
    if self.cb.GetValue():
      print "MEMORIA"


	#informacion del dico duro
def disco():
  global mutex
  mutex.acquire()
  print "/////Disco duro/////\n"
  os.system("du -h") #Descubre archivos mas grandes del sistema
  os.system("tree") #Mostrar los ficheros y carpetas en forma de arbol comenzando por la raiz. (Como git lg)
  mutex.release()
  
	#informacion de la memoria
def memoria():
  global mutex
  mutex.acquire()
  print "/////Memoria/////\n"
 #Se visualiza la cantidad total de memoria libre, la memoria fisica utilizada y el intercambio en el sistema
  os.system("free")
  os.system("cat /proc/meminfo") #Verificar el uso de memoria
  mutex.release()

	#informacio de los procesos
def procesos():
  global mutex
  mutex.acquire()
  print "/////Procesos/////\n"
  os.system("ps")     #Procesos actuales
#para imprimir los procesos en forma de arbol como lo hace el comando que configuramos git lg
  os.system("pstree") 
  mutex.release()
  
 	#informacion del cpu
def cpu():
  global mutex
  mutex.acquire()
  print "/////Informacion del CPU/////\n"
  os.system("cat /proc/cpuinfo")
  mutex.release()

	#Para elgir la Opcion a monitorear
def Opciones(opcion):

  global hilo
  if (opcion == "disco"):
    filament = threading.Thread(target = disco)
    filament.start()
  elif (opcion == "memoria"):
    filament = threading.Thread(target = memoria)
    filament.start()
  elif (opcion == "procesos"):
    filament = threading.Thread(target = procesos)
    filament.start()
  elif (opcion == "cpu"):
    filament = threading.Thread(target = cpu)
    filament.start()
  else:
   print "Intente de nuevo"

def hilo():
  filament0 = threading.Thread(target = disco)
  filament0.start()
  filament1 = threading.Thread(target = memoria)
  filament1.start()
  filament2 = threading.Thread(target = procesos)
  filament2.start()
  filament3 = threading.Thread(target = cpu)
  filament3.start()

def MS():	#MonitorSistema
  global opcion, thr, mutex
  os.system("clear")
  while thr == 0:
      time.sleep(.5)
      print "===>Opciones<===\n"
      print "disco\tmemoria\tprocesos\tcpu"
      opcion = raw_input("ingreseOpcion\t\t")
      Opciones(opcion)
  mutex.release()

MS()		#MonitorSistema
# Estos se ocupan para hacer uso de la ventana con wxpython #
casillasBooleanas = wx.App()
Opciones(None, -1, 'Opcion a monitorear')
casillasBooleanas.MainLoop()
