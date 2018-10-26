#include <stdio.h>
#include <pthread.h>
#include <windows.h>

void *hilo(int *x)
{
	printf("Se crea hilo #%d",&x);
	Sleep(1000);
}

int main(int argc, char* argv[])
{
	int i;
	int a[10];
	
	for(i=0;i<=9;i++)
	{
		//void pthread_create(pthread_t a[i],NULL,hilo,*i);
	}
	/* Este programa es para crear hilos basicos en C,
	pero tengo problemas en los parametros de "pthead_create" */
	
	getchar();
	return 0;
}
