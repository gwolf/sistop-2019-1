PROBLEMA: Santa CLaus
Fuente: Little book of semaphores (Allen B. Downey) (p. 149)

Planteamiento
-Santa Claus duerme en el Polo Norte mientras sus elfos
trabajan frenéticamente en la construcción de millones de
nuevos juguetes.
-A veces se topan con un problema. Pueden pedir ayuda a
Santa Claus, pero sólo de tres en tres.
-Sus nueve renos pasan todo el año de vacaciones en las playas
del Caribe.
-Santa debe despertar a tiempo para iniciar su viaje anual.

Reglas
-Si los nueve renos están de vuelta, es hora de despertar a
Santa Claus para que inicie su recorrido.
-Si los elfos tienen problemas construyendo algún juguete, le
piden ayuda a Santa Claus.
Pero para no darle demasiada lata, lo hacen sólo cuando hay
tres elfos que tienen un problema. Mientras tanto, lo dejan
dormir.
-Puede haber cualquier cantidad de elfos.
_______________________________________________________________

La solución al problema planteado la implementé en Python
Versión del compilador de linux: 2.7.6
_______________________________________________________________

ESTRATEGIA SEGUIDA

Para esta solución, tomé en cuenta que tanto los duendes (elfos)
así como los renos, solicitaban la atención de Santa Claus.
Por ello, definí a Santa Claus como un recurso, limitando su uso
mediante un semáforo, el cuál se vuelve cero cuando atiende al 
grupo de 3 duendes o de 9 renos.
Existe un contador para saber el número de renos que han vuelto,
y un contador para saber cuando 3 duendes están esperando ayuda.
Las modificaciones de cada contador están protegidas mediante un
único mutex.
Finalmente utilicé otro semáforo a manera de torniquete (que en
este caso su función es más similar al de un cadenero). Una vez
que 3 duendes acceden al área de espera, el torniquete se bloquea
hasta que los anteriores salgan. De igual forma, los renos llegan
uno a uno sin necesidad de formarse, hasta que se reunen los 9 y 
solo en ese momento bloquean el torniquete hasta que se adueñan
de Santa.
________________________________________________________________

COMENTARIOS

1. Después de n errores y n correcciones, conocí de cara a los
bloqueos mutuos y a las inaniciones, ya que cuando se implementa
mal el orden de adquisición y liberación de Santa, el Torniquete
y/o el Mutex, un hilo puede estar esperando un recurso A para
liberar el recurso B que posee, mientras que otro hilo esta a la 
espera del recurso B para liberar al A. Luego entonces el proceso
se queda en el limbo eternamente.

2. En la solución actual, cuando se junta el grupo de 3 duendes,
el contador simplemente regresa a 0 para dar espacio a que otro
grupo de 3 duendes esperen por Santa Claus, simulado haber sido
atendidos. Posteriormente se podría implementar una función 
secuencial o por lote (de 3) con la que los duendes interactuen
con Santa Claus antes de volver a sus trabajos.

3. En algún punto entran más de 3 duendes al área de espera.

