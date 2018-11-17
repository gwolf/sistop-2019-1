#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>

char memoria[31];

void inicializarMemoria()
{
    int i=0;
    int indiceABC=0;
    while(i<30)
    {//llena la memoria con procesos de tama;o de memoria aleatorias
        if(rand()%3==0)//1 en 3 de probabilidad para meter un espacio
        {
            int tamEspacio=rand()%4+2;//el espacio tendra un tama;o entre 2 y 5
            int j=0;
            for(j=0;j<tamEspacio;j++)
            {
                memoria[i]='-';
                i++;
                if(i>=30) break;
            }
        }
        else//2 en 3 de probabilidad de que esa region de memoria pertenezca a un proceso
        {
            int tamMemoria=rand()%14+2;
            int j=0;
            for(j=0;j<tamMemoria;j++)
            {
                memoria[i]='A'+indiceABC;
                i++;
                if(i>=30) break;
            }
            indiceABC++;
        }
    }
    memoria[30]='\0';
}

char nombreNuevoProceso()
{
    int i=0, j=0;
    for(i=0;i<30;i++)
    {
        if(memoria[i]>j)
        {
            j=memoria[i];
        }
    }
    return j+1;
}

int buscarPrimerAjuste(int tam)
{
    int i=0,j=0;
    for(i=0;i<30;i++)
    {
        if(memoria[i]=='-')
        {
            j++;
            if(j==tam) return i-tam+1;
        }
        else
        {
            j=0;
        }
    }
    return -1;
}

void compactarMemoria()
{
    int i=0;
    for(i=0;i<30;i++)
    {
        if(memoria[i]=='-')
        {
            int j=i;
            while(j<30 && memoria[j]=='-') j++;
            if(j<30)
            {
                memoria[i]=memoria[j];
                memoria[j]='-';
            }
        }
    }
}

int main()
{
    int respuesta=0;
    srand(time(NULL));
    inicializarMemoria();
    for(;;)
    {
        printf("Asignacion actual:\n\n%s\nAsignar (0) o liberar (1): ",memoria);
        scanf("%i", &respuesta);
        if(respuesta==1)
        {
            printf("Proceso a liberar (ABCDEFGHI): ");
            char proceso[2];
            scanf("%s", proceso);
            int i=0;
            for(i=0;i<30;i++)
            {
                if(memoria[i]==toupper(proceso[0]))
                {
                    memoria[i]='-';
                }
            }
        }
        else
        {
            char nombreX=nombreNuevoProceso();
            printf("Nuevo proceso (%C): ", nombreX);
            scanf("%i", &respuesta);//respuesta=tama;o de memoria del proceso
            while(respuesta < 2 || respuesta > 15)
            {
                printf("valor incorrecto.\nEspecifica el tama;o de memoria del proceso (2-15):");
                scanf("%i", &respuesta);//respuesta=tama;o de memoria del proceso
            }
            int lugarEnMemoria = buscarPrimerAjuste(respuesta);
            if(lugarEnMemoria!=-1)
            {
                int i=0;
                for(i=0;i<respuesta;i++)
                {
                    memoria[lugarEnMemoria+i]=nombreX;
                }
            }
            else
            {
                compactarMemoria();
                printf("*Compactacion requerida*\nNueva situacion:\n%s\nAsignando a %C...\n", memoria, nombreX);
                lugarEnMemoria = buscarPrimerAjuste(respuesta);
                if(lugarEnMemoria!=-1)
                {
                    int i=0;
                    for(i=0;i<respuesta;i++)
                    {
                        memoria[lugarEnMemoria+i]=nombreX;
                    }
                }
                else
                {
                    printf("No hay memoria suficiente para el proceso. Por favor libera uno o varios procesos.\n");
                }
            }
        }
    }
    return 0;
}
