//Modulo de Pruebas
#include <stdio.h>			//biblioteca ANSI C
#include <stdlib.h>			//biblioteca ANSI C
#include <string.h>
#include "ficheros.h"		//biblioteca para el manejo de ficheros en MySis
#include "other.h"			//biblioteca para el uso de comandos de ayuda

void myShell();	            //ejecutara el shell con el que iteractuara el ususario

int main()	
{
	FILE *raiz;
	system("clear");
	printf("**************************************************\n");
	printf("*-------mySys: myShell---------------------------*\n");
    printf("*-------Karla Patricia Guzmán Coronel------------*\n");
	printf("*------------------------------------------------*\n");
	printf("*-------quit: salir-----clean: limpia pantalla---*\n");
	printf("**************************************************\n");
	//creamos archivo que simulara ser el directorio raiz de nuestro sistema de archivos
	raiz = fopen("raiz","w");
	fprintf(raiz, "Root del micro sistema\n");
	fclose(raiz);
	myShell();
	return 0;
}


void myShell(){
	char *command;
	char *arg;
	command = malloc(10*sizeof(char));					   //asignamos memoria para maximo 10 char en cadena de comandos
	arg = malloc(20*sizeof(char));						   //asignamos momoria para maximo 20 chars en cadena de argumentos
	while(command!="quit")   
	{	
		printf("\nmyShell commad ->");					    //muestra la linea que pide nombre de comando	
		fflush(stdin);
		scanf("%s",command);								//recibe comando
			//ejecucion de comandos
		//comandos para ficheros
		//comprueba comando nwefil
		if (strcmp(command,"newfil") == 0){				
			printf("args[name] >>");						
			scanf("%s",arg);								//guardamos arg 
			newfil(arg);									//invocamos al comando ya definido y le pasamos un arg										
		}//fin caso 1
		//comprueba comando readf
		if (strcmp(command,"readf") == 0){					
			printf("args[name] >>");						
			scanf("%s",arg);								 
			readf(arg);																				
		}//fin caso 2
	//otros comandos
	//comprueba comando dtms
		if (strcmp(command,"dtms") == 0)
		{
			dtms();
		}//fin caso 3
	//limpia pantalla
		if (strcmp(command, "clean") == 0){					
			system("clear");
		}//fin caso 4
	//verifica salida
		if(command == ("newfil" || "readf" || "dtms" || "clean")){	 //Comparación de command que no sea cualquier otro. Regresa control a myShell myShell											
			printf("No Valid Command");	                             //comando invalido. Regresa control a myShell
		}//fin caso noValidCommand                      
		if (strcmp(command,"quit") == 0){
				break;										         //cierra myShell; regresa control a main y finaliza ejecucion
		}//fin caso final
		fflush(stdin);
	}
}//fin shell
