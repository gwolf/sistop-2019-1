//Monitor de Sistema 
//Guadarrama Flores Edgar Alejandro
//
#include <pthread.h>
#include <unistd.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gtk/gtk.h>

struct datosProceso {
	char nombre[32];
	char estado[8];
	int nThreads;
	int tamanioMemoria;
};

struct datosSistema {
	int hilosCorriendo;
	int totalSubprocesos;
	float promedioCPU[4];//uso del sistema en promedio de 1 seg y de 1, 5 y 10 minutos
	int ultimoPIDEjecutado;
	char modeloCPU[128];
	int nNucleosVirtuales;
	int nNucleosFisicos;
	char memoriaTotal[64];
	char memoriaLibre[64];
} sistema;

GtkWidget *l_ultimoPID, *l_modeloProcesador, *l_nucleosFisicos, *l_nucleosVirtuales, *l_usoCpu[4];
GtkWidget *l_hilosCorriendo, *l_totalSubprocesos, *l_memoriaTotal, *l_memoriaLibre;

struct datosProceso inspeccionarProcesoID(int pid)//obtiene el nombre, estado, numero de subprocesos y memoria usada por el proceso pid
{
	struct datosProceso tmp;
	tmp.nombre[0]=0;
	tmp.estado[0]=0;
	tmp.nThreads=0;
	tmp.tamanioMemoria=0;
	char sFile[64];
	sprintf(sFile, "/proc/%i/stat", pid);
	if(access(sFile, F_OK) != -1)
	{
		FILE *fp = fopen(sFile,"r");
		fscanf(fp,"%*s %s %s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %i",tmp.nombre, tmp.estado, &tmp.nThreads);
		fclose(fp);
	}
	sprintf(sFile, "/proc/%i/statm", pid);
	if(access(sFile, F_OK) != -1)
	{
		FILE *fp = fopen(sFile,"r");
		fscanf(fp,"%i",&tmp.tamanioMemoria);
		fclose(fp);
	}
	return tmp;
}

void cargaUsoActualCPU()
{
	char sTmp[256];
	long double a[4], b[4];//se toma un promedio del uso del cpu con intervalo de 1 segundo entre muestra y muestra (no recuerdo en que pagina vi que esta era la medida más real)
	FILE *fp = fopen("/proc/stat","r");
	fscanf(fp,"%*s %Lf %Lf %Lf %Lf",&a[0],&a[1],&a[2],&a[3]);
	fclose(fp);
	sleep(1);
	fp = fopen("/proc/stat","r");
	fscanf(fp,"%*s %Lf %Lf %Lf %Lf",&b[0],&b[1],&b[2],&b[3]);
	fclose(fp);
	sistema.promedioCPU[0] = ((b[0]+b[1]+b[2]) - (a[0]+a[1]+a[2])) / ((b[0]+b[1]+b[2]+b[3]) - (a[0]+a[1]+a[2]+a[3])) * 100;
	//actualiza etiqueta de interfaz
	sprintf(sTmp, "%0.2f%%", sistema.promedioCPU[0]);
	gtk_label_set_text(GTK_LABEL(l_usoCpu[0]),sTmp);
}

void cargaUsoPromedioCPU()
{
	char sTmp[256];
	char infoProcesos[32];
	FILE *fp = fopen("/proc/loadavg","r");
	fscanf(fp,"%f %f %f %s %i", &sistema.promedioCPU[1], &sistema.promedioCPU[2], &sistema.promedioCPU[3], infoProcesos, &sistema.ultimoPIDEjecutado);
	fclose(fp);
	sistema.promedioCPU[1]*=100;
	sistema.promedioCPU[2]*=100;
	sistema.promedioCPU[3]*=100;
	strrchr(infoProcesos,'/')[0] = ' ';
	sscanf(infoProcesos,"%i %i", &sistema.hilosCorriendo, &sistema.totalSubprocesos);
	//actualiza etiquetas de interfaz
	sprintf(sTmp, "%0.2f%%", sistema.promedioCPU[1]);
	gtk_label_set_text(GTK_LABEL(l_usoCpu[1]),sTmp);
	sprintf(sTmp, "%0.2f%%", sistema.promedioCPU[2]);
	gtk_label_set_text(GTK_LABEL(l_usoCpu[2]),sTmp);
	sprintf(sTmp, "%0.2f%%", sistema.promedioCPU[3]);
	gtk_label_set_text(GTK_LABEL(l_usoCpu[3]),sTmp);
	sprintf(sTmp, "%i", sistema.hilosCorriendo);
	gtk_label_set_text(GTK_LABEL(l_hilosCorriendo),sTmp);
	sprintf(sTmp, "%i", sistema.totalSubprocesos);
	gtk_label_set_text(GTK_LABEL(l_totalSubprocesos),sTmp);
	sprintf(sTmp, "Último proceso en ejecucion (PID): %i", sistema.ultimoPIDEjecutado);
	gtk_label_set_text(GTK_LABEL(l_ultimoPID),sTmp);
}

void cargaInfoCPU()
{
	char sInfo[256];
	int i=0;
	FILE *fp = fopen("/proc/cpuinfo","r");
	for(i=0;i<16;i++) // Busca linea por linea las palabras clave en este caso sus nucleos y el modelo de procesador
	{
		fgets(sInfo, 256, fp);
		if(strstr(sInfo, "model name")!=NULL)
		{
			strcpy(sistema.modeloCPU, strrchr(sInfo, ':')+1);
		}
		else if(strstr(sInfo, "siblings")!=NULL)
		{
			sistema.nNucleosVirtuales = atoi(strrchr(sInfo, ':')+1);
		}
		else if(strstr(sInfo, "cpu cores")!=NULL)
		{
			sistema.nNucleosFisicos = atoi(strrchr(sInfo, ':')+1);
		}
	}
	fclose(fp);
}

void cargaInfoMemoria()
{
	char sInfo[256];
	int i=0;
	FILE *fp = fopen("/proc/meminfo","r");
	for(i=0;i<16;i++) //Funciona igual que el 'for' anterior
	{
		fgets(sInfo, 256, fp);
		if(strstr(sInfo, "MemTotal")!=NULL)
		{
			char* pTmp = strrchr(sInfo, ':')+1;
			while(pTmp[0]==' ') pTmp++;
			strcpy(sistema.memoriaTotal, pTmp);
		}
		else if(strstr(sInfo, "MemFree")!=NULL)
		{
			char* pTmp = strrchr(sInfo, ':')+1;
			while(pTmp[0]==' ') pTmp++;
			strcpy(sistema.memoriaLibre, pTmp);
		}
	}
	fclose(fp);
	//actualiza etiquetas de interfaz
	gtk_label_set_text(GTK_LABEL(l_memoriaTotal),sistema.memoriaTotal);
	gtk_label_set_text(GTK_LABEL(l_memoriaLibre),sistema.memoriaLibre);
}

int listarProcesos(GtkWidget **listaWidgets)
{
	DIR* proc_dir;
	struct dirent *ent;
	int total = 0;
	proc_dir = opendir("/proc");
	while ((ent = readdir(proc_dir)))
	{
		if ((*ent->d_name>'0') && (*ent->d_name<='9')) // Lista los archivos del directorio /proc 'Solo los archivos que tengan numeros
//									 como nombre seran procesos e ignora a los demas archivos en el directorio'
		{
			listaWidgets[total] = gtk_button_new_with_label(ent->d_name);
			++total;
		}
	}
	closedir(proc_dir);
	return total;
}

void processButtonClick(GtkWidget *widget, gpointer window)
{
	char sTmp[256];
	int pID = atoi(gtk_button_get_label(GTK_BUTTON(widget)));
	struct datosProceso infoProceso = inspeccionarProcesoID(pID);
	sprintf(sTmp, "\nNombre: %s\nEstado: %s\nHilos ejecutandose: %i\nMemoria ocupada: %i\n", infoProceso.nombre, infoProceso.estado, infoProceso.nThreads, infoProceso.tamanioMemoria);
	GtkWidget *dialog;
	dialog = gtk_message_dialog_new(GTK_WINDOW(window),GTK_DIALOG_DESTROY_WITH_PARENT,GTK_MESSAGE_INFO,GTK_BUTTONS_OK,
	sTmp);
	gtk_window_set_title(GTK_WINDOW(dialog), "Informacion del proceso");
	gtk_dialog_run(GTK_DIALOG(dialog));
	gtk_widget_destroy(dialog);
}

void mostrarInterfaz()
{
	char sTmp[256];
	int i=0;
	int totalLista=0;
    GtkWidget *window;
    GtkWidget *granGrid, *myGrid, *procGrid;
    GtkWidget *label2, *label3, *label4, *label5, *label6, *label7, *label8, *label9, *labelA, *labelB, *labelC, *labelD, *labelE;
	GtkWidget *listaWidgets[256];
	
    gtk_init(NULL, NULL);
    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_default_size(GTK_WINDOW(window), 300, 250);

    g_signal_connect(window, "destroy", 
        G_CALLBACK(gtk_main_quit), NULL);

	granGrid = gtk_grid_new();
    myGrid = gtk_grid_new();
	procGrid = gtk_grid_new();
	gtk_grid_set_column_homogeneous(GTK_GRID(myGrid), 1);

	sprintf(sTmp, "Último proceso en ejecucion (PID): %i", sistema.ultimoPIDEjecutado);
    l_ultimoPID = gtk_label_new(sTmp);
	label2 = gtk_label_new("Procesador");
	label3 = gtk_label_new("Uso del CPU");
	label4 = gtk_label_new("Instantaneo:");
	label5 = gtk_label_new("Promedio \núltimo \nminuto:");
	label6 = gtk_label_new("Promedio \núltimos \n5 minutos");
	label7 = gtk_label_new("Promedio \núltimos \n10 minutos");
	label8 = gtk_label_new("Subprocesos");
	label9 = gtk_label_new("Hilos corriendo:");
	labelA = gtk_label_new("Total de subprocesos:");
	labelB = gtk_label_new("Memoria");
	labelC = gtk_label_new("Total");
	labelD = gtk_label_new("Libre");
	labelE = gtk_label_new("Procesos activos");
	l_modeloProcesador = gtk_label_new(sistema.modeloCPU);
	sprintf(sTmp, "Nucleos Fisicos: %i", sistema.nNucleosFisicos);
    l_nucleosFisicos = gtk_label_new(sTmp);
	sprintf(sTmp, "Nucleos Virtuales: %i", sistema.nNucleosVirtuales);
    l_nucleosVirtuales = gtk_label_new(sTmp);
	for(i=0;i<4;i++){
		sprintf(sTmp, "%0.2f%%", sistema.promedioCPU[i]);
		l_usoCpu[i] = gtk_label_new(sTmp);
	}
	sprintf(sTmp, "%i", sistema.hilosCorriendo);
    l_hilosCorriendo = gtk_label_new(sTmp);
	sprintf(sTmp, "%i", sistema.totalSubprocesos);
    l_totalSubprocesos = gtk_label_new(sTmp);
	l_memoriaTotal = gtk_label_new("_");
	l_memoriaLibre = gtk_label_new("_");
	totalLista=listarProcesos(listaWidgets);
    
    gtk_grid_attach(GTK_GRID(myGrid), l_ultimoPID, 2, 0, 3, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label2, 0, 1, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label3, 0, 6, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label4, 1, 7, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label5, 2, 7, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label6, 3, 7, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label7, 4, 7, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label8, 0, 10, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), label9, 1, 11, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), labelA, 2, 11, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), labelB, 0, 14, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), labelC, 1, 15, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), labelD, 2, 15, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), labelE, 0, 18, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), l_modeloProcesador, 1, 2, 3, 1);
	gtk_grid_attach(GTK_GRID(myGrid), l_nucleosFisicos, 1, 3, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), l_nucleosVirtuales, 1, 4, 1, 1);
	for(i=0;i<4;i++) {
		gtk_grid_attach(GTK_GRID(myGrid), l_usoCpu[i], i+1, 8, 1, 1);
	}
	gtk_grid_attach(GTK_GRID(myGrid), l_hilosCorriendo, 1, 12, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), l_totalSubprocesos, 2, 12, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), l_memoriaTotal, 1, 16, 1, 1);
	gtk_grid_attach(GTK_GRID(myGrid), l_memoriaLibre, 2, 16, 1, 1);
	gtk_grid_attach(GTK_GRID(granGrid), myGrid, 0, 0, 1, 1);
	for(i=0;i<totalLista;i++) {
		gtk_grid_attach(GTK_GRID(procGrid), listaWidgets[i], i%17, (i/17)+19, 1, 1);
		g_signal_connect(G_OBJECT(listaWidgets[i]), "clicked", G_CALLBACK(processButtonClick), (gpointer) window);
	}
	gtk_grid_attach(GTK_GRID(granGrid), procGrid, 0, 1, 1, 1);

    gtk_container_add(GTK_CONTAINER (window), granGrid);
    gtk_widget_show_all (window);

	gtk_main();
}

void cargarNuevosDatos()
{/*si creamos un hilo por cada funcion el programa experimenta bugs extraños. Puede ser por hacer llamadas al sistema (fopen) desde
diferentes hilos o lo más probable es que la funcion gtk_label_set_text entre en conflicto al ser llamada desde varios hilos al mismo tiempo
y con diferentes parametros en cuyo caso se desconoce el funcionamiento interno de GTK+ y por tanto no se sabe donde debe ir el mutex
ejemplo de un bug:
*** BUG ***
In pixman_region_append_non_o_: The expression y1 < y2 was false
Set a breakpoint on '_pixman_log_error' to debug
corrupted double-linked list
WidgetsAborted (core dumped)
*/
	for(;;) {
		cargaUsoActualCPU();
		cargaUsoPromedioCPU();
		cargaInfoMemoria();
	}
}

int main(int argc, char *argv[])
{
	if(access("/proc", F_OK) == -1)
	{
		return(1);//no se puede acceder al directorio virtual
	}
	pthread_t t_interfaz, t_stat, t_loadavg, t_meminfo;//un hilo para cada bucle de procesamiento de distinto archivo /proc
	int i=0;
	//inicializar estructura sistema
	sistema.hilosCorriendo=0;
	sistema.totalSubprocesos=0;
	for(i=0;i<4;i++) {
		sistema.promedioCPU[i]=0.0;
	}
	sistema.ultimoPIDEjecutado=0;
	sistema.modeloCPU[0]=0;
	sistema.nNucleosFisicos=0;
	sistema.nNucleosVirtuales=0;
	sistema.memoriaTotal[0]=0;
	sistema.memoriaLibre[0]=0;
	
	/*
		CargaInfoCPU  solo se utilzia una vez, crea la etiqueta ya con el mdoeloCPU, #nucleos fisicos y virtuales llenados
	*/
	cargaInfoCPU();
	pthread_create(&t_interfaz,NULL,(void*)mostrarInterfaz,NULL); 
	/*
		Una vez creados los botnoes y etiquetas se lanzancan los hilos ciclicos para que actualicen los textos de forma independiente
	*/
	pthread_create(&t_stat,NULL,(void*)cargarNuevosDatos,NULL);
	pthread_join(t_interfaz, NULL);//ya que la señal de cerrado del programa le da el hilo interfaz esperamos a que finalice el hilo
	// Esta es la señal de que el usuario dio clicl en la 'x' de cerrar ventana
	return(0);
}
