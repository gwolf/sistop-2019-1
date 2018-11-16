#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define MAX_CONTENT 515
#define MAX_FILENAME 64
#define NOMBRE_ARCHIVO "microsistema.bin"

FILE * pFile;
long lSize;

void limpiarPantalla()
{
    //system("@cls||clear");
    printf("\e[2J\e[H");
    //printf("\n\n\n");
}

int obtenerOpcion()
{
    int respuesta;
    scanf("%i", &respuesta);
    getchar();
    return respuesta;
}

void obtenerContenido(char *destino, int maxSize)
{
    fgets(destino, maxSize, stdin);
    int len=strlen(destino);
    destino[len-1]='\0';
}

int cargarSistema()
{
    pFile = fopen(NOMBRE_ARCHIVO,"a+b");
    if(pFile==NULL)
    {
        printf("Error al tratar de abrir el archivo principal!\n");
        fclose (pFile);
        return 1;
    }
    fseek(pFile, 0, SEEK_END);
    lSize = ftell(pFile);
    return 0;
}

void despliegaMenu()
{
    printf("Microsistema de archivos\n");
    printf("Opciones:\n1.Crear nuevo archivo\n");
    if(lSize>0)
        printf("2.Borrar archivo\n3.Abrir archivo\n4.Listar Archivos\n0.Guardar y salir.\n");
    return;
}

void guardarArchivo(char *Archivo, char *Contenido)
{
    fseek(pFile, 0, SEEK_END);
    int lenFile = strlen(Archivo);
    int lenContent = strlen(Contenido);
    fwrite(&lenFile, sizeof(int), 1, pFile);
    fwrite(Archivo, sizeof(char), lenFile, pFile);
    fwrite(&lenContent, sizeof(int), 1, pFile);
    fwrite(Contenido, sizeof(char), lenContent, pFile);
    lSize = ftell(pFile);
}
int buscarArchivo(char *Archivo)
{
    int lenFile = strlen(Archivo);
    int lenTmp=0;
    char fileName[MAX_FILENAME];
    fseek(pFile, 0, SEEK_SET);
    while(!feof(pFile))
    {
        fread(&lenTmp, sizeof(int), 1, pFile);
        if(feof(pFile))
            break;
        if(lenTmp!=lenFile){
            fseek(pFile, lenTmp, SEEK_CUR);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
            continue;
        }
        else
        {
            fread(fileName, sizeof(char), lenTmp, pFile);
            fileName[lenTmp]='\0';
            if(!strcmp(fileName,Archivo))
            {
                return ftell(pFile)-lenTmp-4;
            }
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
        }
    }
    return -1;
}
void borrarArchivo(char *Archivo)//Crea un duplicado del microsistema pero sin el Archivo que se quiere borrar
{
    FILE * pNuevoArchivo;
    char bufferNuevoArchivo[512];
    int posicionDeCorte = buscarArchivo(Archivo);
    int posicionActual=0;
    if(posicionDeCorte==-1)
    {
        printf("No se encontro el archivo '%s'.\n", Archivo);
        return;
    }
    pNuevoArchivo = fopen("microsistemaTMP.bin","wb");
    if(pNuevoArchivo==NULL)
    {
        printf("Error al tratar de borrar archivo! (no se pudo crear el archivo temporal)\n");
        fclose(pNuevoArchivo);
        return;
    }
    fseek(pFile, 0, SEEK_SET);
    while(!feof(pFile))
    {
        posicionActual+=512;
        if(posicionDeCorte<posicionActual)
        {
            int lenTmp=0;
            posicionActual=ftell(pFile);
            fread(bufferNuevoArchivo, sizeof(char), posicionDeCorte-posicionActual, pFile);
            fwrite(bufferNuevoArchivo, sizeof(char), posicionDeCorte-posicionActual, pNuevoArchivo);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
            posicionDeCorte=99999999;
        }
        int bytesReaded = fread(bufferNuevoArchivo, sizeof(char), 512, pFile);
        fwrite(bufferNuevoArchivo, sizeof(char), bytesReaded, pNuevoArchivo);
    }
    fclose(pNuevoArchivo);
    fclose(pFile);
    if(remove(NOMBRE_ARCHIVO) != 0)
        printf("Error al tratar de borrar archivo!(no se pudo borrar el archivo original)\n");
    else if(rename("microsistemaTMP.bin", NOMBRE_ARCHIVO) != 0){
        printf("Error al tratar de borrar archivo!(no se pudo renombrar el archivo temporal)\n");
        perror("Error");
    }
    else{
        printf("Archivo '%s' borrado!\n", Archivo);
        cargarSistema();
    }
    return;
}  //Hasta aqui copie!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
void listarArchivos()
{
    int lenTmp=0;
    char fileName[MAX_FILENAME];
    limpiarPantalla();
    printf("****** Listado de archivos ******\n\n");
    fseek(pFile, 0, SEEK_SET);
    while(!feof(pFile))
    {
        fread(&lenTmp, sizeof(int), 1, pFile);
        if(feof(pFile))
            break;
        fread(fileName, sizeof(char), lenTmp, pFile);
        fileName[lenTmp]='\0';
        printf("%s\n", fileName);
        fread(&lenTmp, sizeof(int), 1, pFile);
        fseek(pFile, lenTmp, SEEK_CUR);
    }
    printf("\n****** Listado de archivos ******\nPresione enter para regresar al menu principal.");
    getchar();
    return;
}

int main ()
{
    int respuesta=0;
    if(cargarSistema())
        return 1;
regresa:
    despliegaMenu();
    respuesta=obtenerOpcion();
    if((respuesta != 1 && respuesta != 0 && lSize==0) || respuesta < 0 || respuesta > 4)
        printf("No existe esa opcion.");
    else if(respuesta==1)
    {
        char sArchivo[MAX_FILENAME];
        char sContenido[MAX_CONTENT];
        char sOpcion[16];
        printf("Escriba el nombre del archivo que desee crear:\n");
        do{
            obtenerContenido(sArchivo,MAX_FILENAME);
        } while(sArchivo[0]=='\0');
        while(buscarArchivo(sArchivo)!=-1){
            printf("Ese archivo ya existe, elija otro nombre:\n");
            obtenerContenido(sArchivo,MAX_FILENAME);
        }
        printf("Desea escribirlo en este momento?\n1.Si\n2.No\n");
        respuesta=obtenerOpcion();
        sContenido[0]='\0';
        if(respuesta==1)
        {
            limpiarPantalla();
            obtenerContenido(sContenido,MAX_CONTENT);
            strcpy(sOpcion, "escrito");
        }
        else
            strcpy(sOpcion, "creado");
        guardarArchivo(sArchivo, sContenido);
        limpiarPantalla();
        printf("Archivo %s con exito!\n", sOpcion);
        goto regresa;
    }
    else if(respuesta==2)
    {
        char sArchivo[MAX_FILENAME];
        printf("Escriba el nombre del archivo que desee borrar:\n");
        obtenerContenido(sArchivo,MAX_FILENAME);
        limpiarPantalla();
        borrarArchivo(sArchivo);
        goto regresa;
    }
    else if(respuesta==3)
    {
        char sArchivo[MAX_FILENAME];
        printf("Escriba el nombre del archivo que desee abrir:\n");
        obtenerContenido(sArchivo,MAX_FILENAME);
        int addressFile = buscarArchivo(sArchivo);
        if(addressFile!=-1)
        {
            printf("Opciones:\n1.Mostrar contenido\n2.Agregar contenido\n3.Sobreescribir contenido\n");
            respuesta=obtenerOpcion();
            int lenTmp=0;
            char sContenido[MAX_CONTENT];
            fseek(pFile, addressFile, SEEK_SET);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fread(sContenido, sizeof(char), lenTmp, pFile);
            sContenido[lenTmp]='\0';
            limpiarPantalla();
            if(respuesta==1)
            {
                printf("<<%s>>\n%s\n\nPresiona enter para regresar al menu principal.", sArchivo,  sContenido);
                getchar();
                limpiarPantalla();
            }
            else if(respuesta==2)
            {
                borrarArchivo(sArchivo);
                limpiarPantalla();
                printf("Escribe el contenido que deseas agregar:\n");
                obtenerContenido(sContenido+lenTmp,MAX_CONTENT-lenTmp);
                guardarArchivo(sArchivo, sContenido);
                limpiarPantalla();
                printf("Contenido agregado con exito!\n");
            }
            else if(respuesta==3)
            {
                borrarArchivo(sArchivo);
                limpiarPantalla();
                printf("Escribe el contenido que deseas sobreescribir:\n");
                obtenerContenido(sContenido,MAX_CONTENT);
                guardarArchivo(sArchivo, sContenido);
                limpiarPantalla();
                printf("Contenido sobreescrito con exito!\n");
            }
            goto regresa;
        }
        else
        {
            limpiarPantalla();
            printf("El archivo %s no existe!\n", sArchivo);
        }
        goto regresa;
    }
    else if(respuesta==4)
    {
        listarArchivos();
        limpiarPantalla();
        goto regresa;
    }
    else if(respuesta==0)
    {
        printf("Guardando microsistema de archivos y saliendo...\n");
        fclose(pFile);
        return 9;
    }
    return 0;
}
