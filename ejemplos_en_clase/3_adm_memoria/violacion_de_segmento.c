/*  Este programa asigna un arreglo de 10 elementos, y le guarda mucha
 *  más información de la que le cabe. Observen que ante repetidas
 *  ejecuciones, el punto de fallo (el número hasta el cual llega) no
 *  es determinista.
 *
 *  ¿Cómo se comporta si en vez de incrementar el contador i lo
 *  decrementamos? ¿Por qué?
 *
 *  ¿En qué área de la memoria se almacenan las variables "numeritos" e
 *  "i"? ¿Puede eso ayudar a explicar el comportamiento observado?
 */

#include <stdio.h>

void main() {
  int numeritos[10];
  int i=0;
  while (++i) {
    numeritos[i] = i;
    printf("%d...", i);
  }
}
