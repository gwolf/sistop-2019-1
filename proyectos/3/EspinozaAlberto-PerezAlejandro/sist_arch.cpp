#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h> 
#include <ctype.h>
#include <string>

#define LnCad 50  //definicion del tamaño de cadena que se va a manejar

using namespace std;

char CdContenido[LnCad]; 
int NuEstr = 0; //es el contador de estructuras, indica cuantos CdFiles tenemos.

struct StrDat{ //cada CdFile cuenta con dos caracteristicas, un nombre y un CdContenido
	char FlName[70],CdFile[200];
};
int FnCompCh(char* a ,char* b, int t);
void FnHelp();
void FnClear();
void FnSplit(char * original, char * part, int tam, int func);
int FnComand(char cad[LnCad]);

/* se ejecutará el ciclo while hasta que el usuario escriba "salir" */
int main()
{ 
	struct StrDat *StArchivos; //creando un apuntador a estructura StrDat
	StArchivos=(struct StrDat*)calloc(50,sizeof(struct StrDat));
	
	struct user *p; //variable opcion para el inicio, i como contador para señalar en que estructura vamos struct[1], struct[2]...struct[n]
	
	int op=0, contadorC=1, fin=0, j=0;
	char cmd[LnCad], cadFin[]="exit";

	system("cls");

	while(fin==0)
	{
        printf("Root@Winux:~$ "); 
		scanf("\n%[^\n]", cmd); // Escaneamos la cad entera hasta que pulsa intro
		while ((cmd[j]==cadFin[j])&&(cmd[j]!='\0')&&(cadFin[j]!='\0')) // se comparan las cads para ver si se tecleó "exit"
			j++;	
		if ((cmd[j]==cadFin[j])&&(cmd[j]=='\0')&&(cadFin[j]=='\0'))
			exit(0);
		else
		{
			op=FnComand(cmd);
			switch(op)
			{
				case(1):
				{    // se genera una estructura con el nombre del CdFile que estamos definiendo
					strcpy(StArchivos[NuEstr].FlName, CdContenido); 
					NuEstr++; 
					break;
				}
				case(2):
				{   //se realiza una busqueda del nombre del achivo que se quiere eliminar
					char flag='f', CdFile[50];
					int cont=0;
					while((flag=='f') && (cont<NuEstr)){
						strcpy(CdFile, StArchivos[cont].FlName);
						if(strcmp(CdFile,CdContenido)==0){
							flag = 'v';
							//para borrar el CdFile se tiene que reposicionar la estructura a partir del seleccionado
						    for (int i = cont; i < NuEstr; i++)
						    {
						    	strcpy(StArchivos[i].FlName, StArchivos[i + 1].FlName);
						    	strcpy(StArchivos[i].CdFile, StArchivos[i + 1].CdFile);
						    }
						    //reindicamos el tamaño de nuestro arreglo de CdFiles reduciendolo en 1
						    NuEstr--;
						}
						cont++;
					}
					if(flag=='v')
						printf("CdFileivo eliminado.\n");
					else 
						printf("No se localiza el CdFileivo seleccionado.\n");
					break;
				}
				case(3):
				{
					int cont=0;
					char tipo[20];
					while(cont<NuEstr){
						if (strrchr(StArchivos[cont].FlName,'.')==0){ //lista el directorio, si el CdFile no fue definido con 
							strcat(StArchivos[cont].FlName, ".txt"); //alguna extension entonces se define como un .txt
						}else {
							strcpy(tipo,strrchr(StArchivos[cont].FlName,'.'));
						}
						printf("%s\n",StArchivos[cont].FlName);
						cont++;
					}
					break;
				}
				case(4):
				{
					char flag='f', CdFile[200];
					int cont=0;
					while((flag=='f') && (cont<NuEstr)){
						strcpy(CdFile, StArchivos[cont].FlName);
						if(strcmp(CdFile,CdContenido)==0)
							flag = 'v';
						cont++;
					}
					if(flag=='v'){
						system("clear");
						printf("\t\t   --> MODO ESCRITURA <--\n\n"); //se habilita la estructura seleccionada para poder escribir en el CdFile
						scanf("\n%[^\n]",StArchivos[cont].CdFile);
						getchar();
					}else 
						printf("No se localiza el CdFile seleccionado.\n");
					break;
				}
				case(5):
				{
					char flag='f', CdFile[200];
					int cont=0;
					while((flag=='f') && (cont<NuEstr))
					{
						strcpy(CdFile, StArchivos[cont].FlName);
						if(strcmp(CdFile,CdContenido)==0)
							flag = 'v';
						cont++;
					}
					if(flag=='v')
					{
						system("clear");
						printf("\t\t   --> MODO LECTURA <--\n\n"); //se habilita la estructura seleccionada para poder leer el CdContenido del CdFile
						printf("%s\n\n",StArchivos[cont].CdFile);
						getchar();
					}else 
						printf("No se localiza el CdFile seleccionado.\n");
					break;
				}
				case(6):
				{
					char flag='f', CdFile[200], CdFileComp[200];
					int cont=0;
					while((flag=='f') && (cont<NuEstr)){
						strcpy(CdFile, StArchivos[cont].FlName);
						if(strcmp(CdFile,CdContenido)==0)
							flag = 'v';
						cont++;
					}
					if(flag=='v'){
						system("clear");
						printf("\t\t   --> AGREGAR DATOS <--\n\n"); //se habilita la estructura seleccionada para poder leer el contenido del CdFile
						printf("%s\n\n",StArchivos[cont].CdFile);
						scanf("\n%[^\n]",CdFileComp);
						strcat(StArchivos[cont].CdFile, CdFileComp);
						getchar();
					}else 
						printf("No se localiza el CdFile seleccionado.\n");
					//printf("\n%s\n",StArchivos[cont].CdFile);
					break;
				}
				
			}
		}
	}

	exit(1);//finaliza el programa 
	return(0);
}

int FnComand(char cad[LnCad])
{
	char cadFnHelp[]="FnHelp ",cadNuevo[]="new ", cadBorrar[]="kill ", cadLista[]="list", cadEditarEscribir[]="edit -w ", cadEditarLeer[]="edit -r ", cadEditarAnadir[]="edit -a ", clean[]="cls";
	int j=0, func=0;

	if (FnCompCh(cadNuevo,cad,4)==1){
		cout<<" A   "<<FnCompCh(cadNuevo,cad,4)<<endl;
		FnSplit(cad,cadNuevo,4,1);
		func = 1;
	}else if (FnCompCh(cadLista,cad,4)==1){
		cout<<" B   "<<FnCompCh(cadLista,cad,5)<<endl;
		func = 3;
	}else if (FnCompCh(cadBorrar,cad,5)==1){
		FnSplit(cad,cadBorrar,5,2);
		func = 2;
	}else if (FnCompCh(cadEditarEscribir,cad,8)==1){
		FnSplit(cad,cadEditarEscribir,8,4);
		func = 4;
	}else if (FnCompCh(cadEditarLeer,cad,8)==1){
		FnSplit(cad,cadEditarLeer,8,5);
		func = 5;
	}else if (FnCompCh(cadEditarAnadir,cad,8)==1){
		FnSplit(cad,cadEditarAnadir,8,6);
		func = 6;
	}else if (FnCompCh(clean,cad,2)==1){
		FnClear();
	}else if (FnCompCh(cadFnHelp,cad,3)==1){
		FnHelp();
	}else{
		printf("No se reconoce el comando. Leer documentacion.\n");
	}

	return func;
}

void FnSplit(char* original, char* part, int tam, int func)
{
    //char original[] = "funciona chido";
    //char part[] = "funciona ";
    char nueva[21];
    int posicion = strlen(original)-strlen(strstr(original, part));

    // copiar la primera part
    for(int a = 0; a < posicion; a++)
        nueva[a] = original[a];
    // copiar la segunda part
    for(int a = posicion; a < strlen(original); a++)
        nueva[a] = original[a+tam]; 
    nueva[20] = '\0';
    strcpy(CdContenido,nueva);
}
int FnCompCh(char* a ,char* b, int t){
	int i=0;
	while ( i < t)
	{
		if(a[i]==b[i]){
			i++;
		}else {
		return 0;
		}
	}return 1;
}
void FnClear(){
	system("cls");
}
void FnHelp()
{
	system("clear");

	printf("\t\tMANUAL DE USO:\n");
	printf("el sistema consiste en administrar CdFiles, permitiendo las siguientes acciones: \n");
	printf("\t- crear\n\t- listar\n\t- escribir\n\t- leer\n\t- agregar\n");
	printf("para poder ejecutar cualquiera de las acciones es necesario seguir la siguiente estructura de funciones:\n");
	printf("\n\t- new nombre.tipo --> para crerar un nuevo CdFile, sino se especifica la extension del CdFile el sistema genera un CdFile .txt\n");
	printf("\n\t- list --> para listar los elementos del directorio, la funcion no requiere argumentos.\n");
	printf("\n\t- erase nombre.tipo --> para eliminar algun CdFile del directorio, es necesario especificar nombre y tipo de CdFile como argumento.\n");
	printf("\n\t- edit -w nombre.tipo --> abre el editor en modo escritura, es necesario especificar -w para indicar el modo escritura asi como nombre y");
	printf("tipo de CdFile. Despliega una pantalla donde queda habilitada la escritura en el CdFile y para salir solo es necesario presionar la tecla ENTER\n");
	printf("\n\t- edit -w nombre.tipo --> abre el editor en modo escritura, es necesario especificar -w para indicar el modo escritura asi como nombre y");
	printf("tipo de CdFile. Despliega una pantalla donde queda habilitada la escritura en el CdFile y para salir solo es necesario presionar la tecla ENTER\n");
	printf("\n\t- edit -r nombre.tipo --> abre el editor en modo lectura, es necesario especificar -r para indicar el modo lectura asi como nombre y");
	printf("tipo de CdFile. Despliega una pantalla con el contenido del CdFile y para salir solo es necesario presionar la tecla ENTER\n");
	printf("\n\t- edit -a nombre.tipo --> abre el editor para agregar informacion, es necesario especificar -a para indicar que se quiere agregar y");
	printf("no sobrescribir asi como nombre y tipo de CdFile. Despliega una pantalla donde podremos agregar informacion al CdFile y para salir solo es necesario presionar la tecla ENTER\n");
	printf("\n\t- exit --> para salir del programa, termina la ejecucion\n\n\n");
}
