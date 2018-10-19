#include <string.h>
#include <stdlib.h>
#include <stdio.h>

int main(int ARGC, char **ARGV) {
  char nombre = 20;
  if (ARGC < 2) {
    printf("Debes indicarme el nombre\n");
    exit(1);
  } else {
    printf("Recibí %d argumentos\n", ARGC);
  }
  strncpy(&nombre, ARGV[0], 20);
  printf("¡Hola %s!\n", nombre);
  exit(0);
}
