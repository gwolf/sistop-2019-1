	 PROYECTO #2
MONITOR DEL SISTEMA OPERATIVO

SISTEMAS OPERATIVOS SEMESTRE 2019-1
PROFESOR: GUNNAR WOLF

ALUMNOS: RAMÍREZ ANCONA SIMÓN EDUARDO
	 VALRIANO BARRIOS CRISTIAN
ENTREGA: 18/10/2018
________________________________________

REQUISITOS:
Python versión 2.7.6 en adelante
________________________________________

ACERCA DE SU FUNCIONAMIENTO:

Para este monitor del sistema operativo, 
la estructura está basada en el código
contenido en el repositorio:
https://github.com/juanpflores/monitor

Sin embargo, el código en cuestión no
implementa correctamente la sincronización
entre hilos.

En nuestro caso, para nuestra implementación
decidimos sincronizar la impresión de los
procesos mediante un mutex.
Decidimos que los hilos que muestran el uso
de la memoria, y el que muestra los procesos
activos, deberían actualizarse constantemente.
Consideramos que el resto de los hilos no 
requieren una actualización automática ni sería
tan interesante hacerlo.

Los hilos que actualizan su información lo hacen 
mediante un bucle ligado a una variable de
condición propia (pero global) del hilo.
Antes de tomar el mutex, detiene los bucles externos 
y reinician la variable de condición propia para 
poder iniciar su propio bucle.
Una vez que finaliza cada ciclo, el mutex se libera y
el hilo duerme una pequeña cantidad de tiempo para dar
oportunidad al usuario de solicitar otro hilo.
Si nadie pide el mutex, el siguiente ciclo lo
adquiere de nuevo.

En nuestro caso particular, los hilos son
lanzados e inicializados cuando el usuario los
solicita desde el shell, no sin antes liberar
al mutex, en caso de que alguno de los hilos
que NO se están actualizando lo esté utilizando,
y así cada función puede tomarlo.



