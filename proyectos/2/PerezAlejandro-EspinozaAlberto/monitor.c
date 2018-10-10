#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> //Uso de 'tuberías'/pipes
#include <fcntl.h> //Maneja el descriptor de archivos
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <signal.h> //Uso de señales
#include <pthread.h> //Uso de hilos

#define cad 50

void prompt(int tipo);
void entrada(char arch[cad]);
void salida(char arch[cad]);
void Error(char arch[cad]);
void pipes(char* firstInstP[cad], char* secInstP[cad]);
void newProcess(char* firstInstP[cad]);
void instruccion(char cadena[cad]);

int main()
{
	pthread_t thread;
	int fin=0, out=dup(1), in=dup(0), error=dup(2);
	int j=0;
	char commd[cad], cadFin[]="exit";

	while(fin==0)
	{
		close(1);
		dup(out);
		close(0);
		dup(in);
		close(2);
		dup(error);
		signal(SIGINT, prompt);
		prompt(0);
		scanf("\n%[^\n]", commd);
		if (strcmp(commd, cadFin)==0) //Se comparan las cadenas 'commd' y 'cadFin' y si son iguales, termina el programa
			exit(1);
		instruccion(commd);
	}
}

void prompt(int tipo)
{
	switch(tipo)
	{
		case 2:
			printf("User2~>");
		break;
		default:
			printf("User~>");
	}
}

void entrada(char arch[cad])
{
	char *archP;
	int fd;

	archP=arch;
	fd=open(archP, O_RDONLY);
	close(0);
	dup(fd);
}

void salida(char arch[cad])
{
	char *archP;

	archP=arch;
	close(1);
	open(archP, O_CREAT | O_WRONLY);
}

void Error(char arch[cad])
{
	char *archP;

	archP=arch;
	close(2);
	open(archP, O_CREAT | O_WRONLY);
}

void pipes(char* firstInstP[cad], char* secInstP[cad])
{
	int fd[2], estado;
	pid_t child;

	pipe(&fd[0]);
	child=fork();

	if(child == -1)
		printf("ERROR, no se pudo crear proceso.");
	else if(child==0)
	{
		//pipe(&fd[0]);
		if(fork()!=0)
		{
			close(fd[0]);
			close(1);
			dup(fd[1]);
			close(fd[1]);
			execvp(firstInstP[0], firstInstP);
			perror("No se encontro la instruccion");
			exit(estado);
		}
		else
		{
			close(fd[1]);
			close(0);
			dup(fd[0]);
			close(fd[0]);
			execvp(secInstP[0], secInstP);
			perror("No se encontro la instruccion");
			exit(estado);
		}
	}
	else
		child=wait(&estado);
}

void newProcess(char* firstInstP[cad])
{
	int estado;
	pid_t child;

	child=fork();
	if(child == -1)
		printf("ERROR, no se pudo crear proceso.");
	else if(child==0)
	{
		execvp(firstInstP[0], firstInstP);
		perror("No existe la instruccion");
	}
	else
		child=wait(&estado);
}

void instruccion(char cadena[cad])
{
	char firstInst[cad][cad], secInst[cad][cad], changeOut[cad], changeIn[cad];
	char *firstInstP[cad], *secInstP[cad];
	int ejec=0, i, j, k, usePipe=0;

	firstInstP[0]=NULL;
	secInstP[0]=NULL;
	i=0;
	k=0;

	while(cadena[i]!='\0' && cadena[i]!='|' && cadena[i]!='>' && cadena[i]!='2')
	{
		for(j=0; cadena[i]!=' ' && cadena[i]!='\0' && cadena[i]!='|' && cadena[i]!='>' && cadena[i]!='<'; j++)
		{
			firstInst[k][j]=cadena[i];
			i++;
		}
		if(cadena[i]==' ')
			i++;
		firstInst[k][j]='\0';
		firstInstP[k]=firstInst[k];
		k++;
		if(cadena[i]=='<')
		{
			i++;
			if(cadena[i]!=' ')
				ejec=1;
			else
			{
				i++;
				for(j=0; cadena[i] != '\0' && cadena[i] != ' ' && cadena [i] != '|' && cadena [i] != '>'; j++)
				{
					changeIn[j]='\0';
					i++;
				}
				changeIn[j]='\0';
				if(cadena[i]!='\0')
					i++;
				entrada(changeIn);
			}
		}
	}
	firstInstP[k]=NULL;
	if(cadena[i]=='>')
	{
		i++;
		if(cadena[i]!=' ')
			ejec=1;
		else
		{
			i++;
			for(j=0; cadena[i]!='\0'; j++)
			{
				changeOut[j]=cadena[i];
				i++;
			}
			changeOut[j]='\0';
			salida(changeOut);
		}
	}
	if(cadena[i]=='2' && cadena[i+1]=='>')
	{
		i++;
		i++;
		if(cadena[i]!=' ')
			ejec=1;
		else
		{
			i++;
			for(j=0; cadena[i]!='\0'; j++)
			{
				changeOut[j]=cadena[i];
				i++;
			}
			changeOut[j]='\0';
			Error(changeOut);
		}
	}
	if(cadena[i]=='|')
	{
		k=0;
		i++;
		if(cadena[i]!=' ')
			ejec=1;
		else
		{
			i++;
			usePipe=1;
			while(cadena[i]!='\0' && cadena[i]!='>')
			{
				for(j=0; cadena[i] != ' ' && cadena[i] != '\0' && cadena[i] != '>'; j++)
				{
					secInst[k][j]=cadena[i];
					i++;
				}
				if(cadena[i]==' ')
					i++;
				secInst[k][j]='\0';
				secInstP[k]=secInst[k];
				k++;
			}
			secInstP[k]=NULL;
		}
	}
	if(ejec==0)
	{
		if(usePipe==0)
			newProcess(firstInstP);
		else
			pipes(firstInstP, secInstP);
	}
	else
		printf("Error de sintaxis.");
}