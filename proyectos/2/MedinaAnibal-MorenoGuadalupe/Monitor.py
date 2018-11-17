#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import subprocess
import time
import sys
import threading
import psutil

# Numero de nucleos que tiene nuestra computadora
NumNucleos = int(subprocess.getoutput("grep processor /proc/cpuinfo | wc -l"))

# Mutex para proteger al contador
mutex = threading.Semaphore(1)
aviso = threading.Semaphore(1)
global contahilos
contahilos = 0

# Semáforo para señalizar que todos los hilos cumplieron con su funcion
signal = threading.Semaphore(0)



# señalizar entre hilos
def alertProces():
	# Adquirimos el mutex para escritura y lectura de la variable contador de hilos
	aviso.acquire()
	global contahilos
	contahilos += 1
	if contahilos == func_monitor:
		signal.release()
	# Se libera mutex
	aviso.release()



# Se da el modelo del CPU de la computadora donde se corra el programa
def modeloCPU():
    # Guardamos lo que haya en /proc/cpuinfo y filtramos el apartado donde diga el modelo
    modelo = subprocess.getoutput("cat /proc/cpuinfo | grep -e 'model\ name'")
    modeloFiltro = ""
    for i in modelo:
        if i == '\n':
            modeloFiltro = modeloFiltro.replace("model name\t: ","")
            return modeloFiltro
        modeloFiltro += i

# obtener el kernel del SO
def kernel():
    version_so = subprocess.getoutput("cat /proc/version | while read c1 c2 c3 c4; do echo $c1 $c2 $c3; done")
    return version_so



#saber el porcentaje de uso del cpu que está manejando el Usuario
def Usuario():
    cpu1 = subprocess.getoutput("cat /proc/stat | grep 'cpu ' | while read c1 c2 c3; do echo $c2; done")
    time.sleep(1)
    cpu2 = subprocess.getoutput("cat /proc/stat | grep 'cpu ' | while read c1 c2 c3; do echo $c2; done")
    # calculamos el tiempo tomando dos muestreos con un segundo de diferencia y se divide entre el número de nucleos
    cpu_uso = (int(cpu2) - int(cpu1)) / numNucleos
    alertProces()
    return str(cpu_uso)

# saber el porcentaje de uso del cpu que está manejando el Sistema
def Sistema():
    estado1 = subprocess.getoutput("cat /proc/stat | grep 'cpu ' | while read c1 c2 c3 c4 c5; do echo $c4; done")
    time.sleep(1)
    estado2 = subprocess.getoutput("cat /proc/stat | grep 'cpu ' | while read c1 c2 c3 c4 c5; do echo $c4; done")
    cpu_uso = (int(estado2) - int(estado1)) / NumNucleos
    alertProces()
    return str(cpu_uso)

# saber el porcentaje de uso que está Inactivo
def cpuInactivo():
    estado1 = subprocess.getoutput("cat /proc/stat | grep 'cpu ' | while read c1 c2 c3 c4 c5 c6; do echo $c5; done")
    time.sleep(1)
    estado2 = subprocess.getoutput("cat /proc/stat | grep 'cpu ' | while read c1 c2 c3 c4 c5 c6; do echo $c5; done")
    cpu_uso = (int(estado2) - int(estado1)) / NumNucleos
    alertProces()
    return str(cpu_uso)



# memoria total que tiene nuestra computadora, se muestra en kB
def MemoTotal():
    memtotal =  subprocess.getoutput("cat /proc/meminfo | while read c1 c2; do echo $c2; done | sed -n '1 p'")
    alertProces()
    return memtotal

# memoria libre que tiene nuestra computadora( se muestra en kB)
def MemoLibre():
    memlibre =  subprocess.getoutput("cat /proc/meminfo | while read c1 c2; do echo $c2; done | sed -n '2 p'")
    alertProces()
    return memlibre

# memoria que está usando el usuario(se muestra en kB)
def MemoUso():
    memuso =  subprocess.getoutput("cat /proc/meminfo | while read c1 c2; do echo $c2; done | sed -n '7 p'")
    alertProcess()
    return memuso

# memoria de intercambio total que tiene nuestra computadora(se muestra en kB)
def MemoSwapTotal():
    memswap =  subprocess.getoutput("cat /proc/meminfo | while read c1 c2; do echo $c2; done | sed -n '19 p'")
    alertProces()
    return memswap

# memoria de intercambio libre que tiene nuestra computadora(se muestra en kB)
def MemoSwapLibre():
    memswaplibre =  subprocess.getoutput("cat /proc/meminfo | while read c1 c2; do echo $c2; done | sed -n '20 p'")
    alertProces()
    return memswaplibre

# memoria de intercambio que está usando(se muestra en kB)
def MemoSwapUso():
    memswapuso =  subprocess.getoutput("cat /proc/meminfo | while read c1 c2; do echo $c2; done | sed -n '6 p'")
    alertProces()
    return memswapuso



# número de procesos que tenemos
def NumProcesos():
    numprocesos = subprocess.getoutput("cat /proc/loadavg | grep -o '/[0-9]*'")
    # Filtramos la información inutil
    numprocesos = numprocesos[1:]
    alertProces()
    return numprocesos

# número de procesos que estén ejecutandose en este momento
def NumProcEjecucion():
    numprocesos = subprocess.getoutput("cat /proc/loadavg | grep -o '[0-9]*/'")
    numprocesos = numprocesos[:-1]
    alertProces()
    return numprocesos



# convertir los segundos en un formato de HH:MM:SS para mayor estetica al momento de mostrarlo
def horaCompleta(segundos):
    # Para saber las horas dividimos los segundos entre 3600, muy importante hacerlo con el doble diagonal, para división entera
    horas = segundos // 3600
    # Agregamos un 0 en caso de que las horas no acompleten la decena
    if horas < 10:
        horas = '0' + str(horas)
    # Para saber los minutos divimos el residuo de lo que quedó de las horas entre 60
    minutos = (segundos % 3600) // 60
    # Agregamos un 0 en caso de que los minutos no acompleten la decena
    if minutos < 10:
        minutos = '0' + str(minutos)
    # Para calcular los segundos sacamos el modulo del residuo, lo que asegura que que no será ni horas ni minutos
    segundos = (segundos % 3600) % 60
    # Agregamos un 0 en caso de que los segundos no acompleten la decena
    if segundos < 10:
        segundos = '0' + str(segundos)
    # Retornamos la hora en formato HH:MM:SS
    return str(horas) + ":" + str(minutos) + ":" + str(segundos)

# tiempo que ha estado encendido el sistema
def tFuncionamiento():
    tfuncionamiento = subprocess.getoutput("cat /proc/uptime | while read c1 c2; do echo $c1; done")
    # Filtramos el tiempo ignorando a partir del punto decimal(los últimos 3 digitos), lo convertimos en entero
    tfuncionamiento = int(tfuncionamiento[:-3])
    # Transformamos los segundos en un formato más presentable
    tfuncionamiento = horaCompleta(tfuncionamiento)
    alertProces()
    return tfuncionamiento

# tiempo que ha estado inactivo el sistema
def tInactivo():
    tinac = subprocess.getoutput("cat /proc/uptime | while read c1 c2; do echo $c2; done")
    # Filtramos el tiempo ignorando a partir del punto decimal(los últimos 3 digitos), lo convertimos en entero
    tinac = int(tinac[:-3])
    # Transformamos los segundos en un formato más presentable
    tinac = horaCompleta(tinac)
    alertProces()
    return tinac



# listar los procesos que tengamos, hacemos uso del módulo "psutil"
def listProces():
    username = []
    pid = []
    nombre = []
    status = []
    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username','status'])
        for llave,valor in pinfo.items():
            if llave == 'username':
                username.append(valor)
            elif llave == 'pid':
                pid.append(valor)
            elif llave == 'name':
                nombre.append(valor)
            elif llave == 'status':
                status.append(valor)
    alertProces()
    return [len(username),username,pid,nombre,status]



funcionesALanzar = [cpuUsuario, cpuSistema,cpuInactivo, memTotal,memLibre,memUso,memSwapTotal,memSwapLibre,memSwapUso,numProcesos,numProcEjecucion,tFuncionamiento,tInactivo,listaProc]
func_monitor = len(funcionesALanzar)

# lanzar los hilos
def iniciaHilos():
    for i in funcionesALanzar:
        threading.Thread(target = i).start()



# interfaz gráfica con tkinter
def interfaz():
	contenedor = Tk()
	contenedor.title("Monitor")
	frame = Frame(contenedor,heigh=600,width=500)
	frame.pack(padx=20,pady=20)
	frame.configure(bg = "black")

	Label(frame,text="*Características",fg="red",font="Verdana 10",bg="black").place(x=0,y=0)
	Label(frame,text="Kernel:   " +  kernel(),font="Verdana 10",bg="black",fg="white").place(x=0,y=20)
	Label(frame,text="Procesador:   " + modeloCPU(),font="Verdana 10",bg="black",fg="white").place(x=0,y=40)
	Label(frame,text="-----------------------------------------------------------------------------------------------------------------------------",bg="black",fg="white").place(x=0,y=60)
	Label(frame,text="*Memoria",font="Verdana 10",bg="black",fg="red").place(x=0,y=80)
	Label(frame,text="memoria: ",font="Verdana 10",bg="black",fg="white").place(x=0,y=100)
	Label(frame,text=MemoTotal() + " Total",font="Verdana 10",bg="black",fg="white").place(x=80,y=100)
	Label(frame,text=MemoLibre() + " Libre",font="Verdana 10",bg="black",fg="white").place(x=210,y=100)
	Label(frame,text=MemoUso() + " En uso",font="Verdana 10",bg="black",fg="white").place(x=340,y=100)
	Label(frame,text="swap: ",font="Verdana 10",bg="black",fg="white").place(x=0,y=120)
	Label(frame,text=MemoSwapTotal() + " Total",font="Verdana 10",bg="black",fg="white").place(x=80,y=120)
	Label(frame,text=MemoSwapLibre() + " Libre",font="Verdana 10",bg="black",fg="white").place(x=210,y=120)
	Label(frame,text=MemoSwapUso() + " En uso",font="Verdana 10",bg="black",fg="white").place(x=340,y=120)
	Label(frame,text="-----------------------------------------------------------------------------------------------------------------------------",bg="black",fg="white").place(x=0,y=140)
	Label(frame,text="*CPU",font="Verdana 10",bg="black",fg="red").place(x=0,y=160)
	Label(frame,text="%CPU:",font="Verdana 10",bg="black",fg="white").place(x=0,y=180)
	Label(frame,text=Usuario()+"% Uso",font="Verdana 10",bg="black",fg="white").place(x=80,y=180)
	Label(frame,text=Sistema()+"% Sys",font="Verdana 10",bg="black",fg="white").place(x=210,y=180)
	Label(frame,text=cpuInactivo()+"% Inac",font="Verdana 10",bg="black",fg="white").place(x=340,y=180)
	Label(frame,text="Tiempo: ",font="Verdana 10",bg="black",fg="white").place(x=0,y=200)
	Label(frame,text=tFuncionamiento()+" Funcionando",font="Verdana 10",bg="black",fg="white").place(x=120,y=200)
	Label(frame,text=tInactivo()+" Inactivo",font="Verdana 10",bg="black",fg="white").place(x=320,y=200)
	Label(frame,text="-----------------------------------------------------------------------------------------------------------------------------",bg="black",fg="white").place(x=0,y=220)
	procesosListado = listProces()
	Label(frame,text="*Procesos",font="Verdana 10",bg="black",fg="red").place(x=0,y=240)
	Label(frame,text="Total:",font="Verdana 10",bg="black",fg="white").place(x=0,y=260)
	Label(frame,text=procesosListado[0],font="Verdana 10",bg="black",fg="white").place(x=80,y=260)
	Label(frame,text="Activos: ",font="Verdana 10",bg="black",fg="white").place(x=250,y=260)
	Label(frame,text="Username ",font="Verdana 10",bg="black",fg="cyan").place(x=0,y=290)
	Label(frame,text="PID ",font="Verdana 10",bg="black",fg="cyan").place(x=125,y=290)
	Label(frame,text="Nombre ",font="Verdana 10",bg="black",fg="cyan").place(x=250,y=290)
	Label(frame,text="Estado ",font="Verdana 10",bg="black",fg="cyan").place(x=375,y=290)
	Button( text='Salir', command=quit, bg="black",fg="white", relief="raised", bd=5).pack(side=RIGHT)
	Button( text='Actualizar', command=contenedor.destroy, bg="black",fg="white", relief="raised", bd=5).pack(side=RIGHT)
	ejex = 0
	for i in range(1,len(procesosListado)):
	    ejey = 310
	    for j in range(procesosListado[0]):
	        Label(frame,text=procesosListado[i][j],font="Verdana 10",bg="black",fg="white").place(x=ejex,y=ejey)
	        ejey += 20
	    ejex += 125
	frame.mainloop()





def main():
	global conthilos
	while True:
		iniciaHilos()
		# Espera a que todos los hilos terminen
		print("una vez")
		signal.acquire()
		interfaz()
		# Mutex para reiniciar contador
		mutex.acquire()
		contahilos = 0
		mutex.release()



# Ejecución del programa
main()
