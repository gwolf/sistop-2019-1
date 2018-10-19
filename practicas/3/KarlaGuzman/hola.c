/*programa hola mundo
hecho por karla*/

#include <stdio.h> //printf y getchar
#include <stdlib.h>

int main (int argc, char** argv)
{
	printf ("hola mundo");
	
	fflush(stdin); //limpia buffer del teclado
	getchar(); //mantiene pantalla estática
	return 0; //termina ejecucion devolviendo cero
} //cierra f principal
