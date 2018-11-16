/*
El microsistema de archivos funciona en base a un archivo binario con el siguiente formato para separar los archivos.
|longitudNombreArchivo1(4 bytes)|NombreArchivo1(lonNombArch1 bytes)|longitudContenidoArchivo1(4 bytes)|ContenidoArchivo1(lonContArch1 bytes)|LNA2|NA2|LCA2|CA2|LNA3|NA3|LCA3|CA3|...
*/

#include <stdio.h>
#include <string.h>
#include <unistd.h>
//#include <windows.h> //para windows



#define MAX_CONTENT 515
#define MAX_FILENAME 64
#define NOMBRE_ARCHIVO "microsistema.bin"

FILE * pFile;
long lSize;//variable de apoyo para saber si hay almenos 1 archivo en nuestro sistema de archivos

void limpiarPantalla()
{
    printf("\e[2J\e[H");
    //("@cls||clear");  //Para windows y se limpie la pantalla cada que terminamos una instruccion
}

int obtenerOpcion()
{
    int respuesta;
    scanf("%i", &respuesta);
    getchar();//se utiliza getchar adicional para que no proceso la tecla Enter
    return respuesta;
}

void obtenerContenido(char *destino, int maxSize)
{
    fgets(destino, maxSize, stdin);//se utiliza para obtener un texto incluyendo espacios hasta que se presione enter
    int len=strlen(destino);
    destino[len-1]='\0';
}

int cargarSistema()
{
    pFile = fopen(NOMBRE_ARCHIVO,"a+b");//se abre el archivo en modo apertura binaria para agregar contenido(nuevos archivos) y guardar variables en modo binario
    if(pFile==NULL)
    {
        printf("Error al tratar de abrir el archivo principal!\n");
        fclose (pFile);
        return 1;
    }
    fseek(pFile, 0, SEEK_END);//se posiciona al final del archivo para cuando se cree un nuevo archivo se coloque hasta el final
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
    fwrite(&lenFile, sizeof(int), 1, pFile);//se guardan en 4 bytes la longitud del nombre del archivo
    fwrite(Archivo, sizeof(char), lenFile, pFile);//se guarda el nombre del archivo
    fwrite(&lenContent, sizeof(int), 1, pFile);//se guarda en 4 byte la longitud del contenido
    fwrite(Contenido, sizeof(char), lenContent, pFile);//se guarda el contenido del archivo
    lSize = ftell(pFile);
}
int buscarArchivo(char *Archivo)
{/*para buscar un archivo en especifico empezamos a recorrer nuestro archivo binario
buscando que la longitud del nombre de archivo que buscamos coincida con la longitud del nombre de alguno de nuestros archivos guardados.
En caso que coincida entonces se lee el nombre del archivo y se compara con el que buscamos.
Si coinciden los nombres es porque encontramos el archivo y la funcion retorna la posicion de nuestro .bin en la cual se encuentra el archivo.
De lo contrario retorna -1 en señal de que no se encontro.
*/
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
{/* Se podria usar un sistema como en la tarea2 manejando la memoria, buscar huecos, comparar, compactar, etc... Pero se volveria muy complejo
y requeriria bastante tiempo el desarrollarlo. Por lo que se opto por la manera mas sencilla (duplicar omitiendo el archivo que se quiere borrar).
*/
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
    while(!feof(pFile))//el duplicado se crea copiando 512 bytes por cada ciclo del while hasta que se llegue al final del archivo.
    {
        posicionActual+=512;
        if(posicionDeCorte<posicionActual)//si la posicion del archivo que queremos borrar se encuentra en el bloque de 512 bytes actual, entonces leemos hasta donde comienza este
        {//y continuamos n bytes despues (donde terminan los datos del archivo que queremos borrar) (n=4bytes+longitudNombre+4bytes+longitudContenido)
            int lenTmp=0;
            posicionActual=ftell(pFile);
            fread(bufferNuevoArchivo, sizeof(char), posicionDeCorte-posicionActual, pFile);
            fwrite(bufferNuevoArchivo, sizeof(char), posicionDeCorte-posicionActual, pNuevoArchivo);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
            posicionDeCorte=99999999;//una vez que nos saltamos el archivo borrado, ya no comparamos el resto y nos dedicamos a solo copiar el resto de nuestro microsistema.
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
}
void listarArchivos()
{/*para listar los archivos: leemos 4 bytes, leemos el nombre del archivo con la longitud obtenida, leemos 4 bytes,
saltamos la longitud que nos dieron estos ultimos 4 bytes y repetimos hasta el final del microsistema*/
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
    printf("\n****** Fin del listado de archivos ******\nPresione enter para regresar al menu principal.");
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
    if((respuesta != 1 && respuesta != 0 && lSize==0) || respuesta < 0 || respuesta > 4)//si no tenemos archivos en nuestro microsistema entonces solo mostraremos la opcion 1 (crear nuevo archivo)
	{
        printf("No existe esa opcion.");
		despliegaMenu();
	}
    else if(respuesta==1)//la siguientes 2 opciones se sobreentienden en el codigo
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
    else if(respuesta==3)//si selecciona abrir el archivo:
    {
        char sArchivo[MAX_FILENAME];
        printf("Escriba el nombre del archivo que desee abrir:\n");
        obtenerContenido(sArchivo,MAX_FILENAME);
        int addressFile = buscarArchivo(sArchivo);
        if(addressFile!=-1)
        {
            printf("Opciones:\n1.Mostrar contenido\n2.Agregar contenido\n3.Sobreescribir contenido\n");//mostramos las opciones que se pueden hacer con ese archivo
            respuesta=obtenerOpcion();
            int lenTmp=0;
            char sContenido[MAX_CONTENT];//leemos el contenido por anticipado (lo utilizaremos independientemente de la opcion seleccionada).
            fseek(pFile, addressFile, SEEK_SET);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fseek(pFile, lenTmp, SEEK_CUR);
            fread(&lenTmp, sizeof(int), 1, pFile);
            fread(sContenido, sizeof(char), lenTmp, pFile);
            sContenido[lenTmp]='\0';
            limpiarPantalla();
            if(respuesta==1)//la mas facil. Solo mostramos el contenido
            {
                printf("<<%s>>\n%s\n\nPresiona enter para regresar al menu principal.", sArchivo,  sContenido);
                getchar();
                limpiarPantalla();
            }
            else if(respuesta==2)//Se puede hacer algo mas elaborado pero por simplicidad:
            {//ya tenemos el contenido, entonces borramos el archivo, agregamos lo que el usuario escribio y lo guardamos como si fuera un nuevo archivo
                borrarArchivo(sArchivo);
                limpiarPantalla();
                printf("Escribe el contenido que deseas agregar:\n");
                obtenerContenido(sContenido+lenTmp,MAX_CONTENT-lenTmp);
                guardarArchivo(sArchivo, sContenido);
                limpiarPantalla();
                printf("Contenido agregado con exito!\n");
            }
            else if(respuesta==3)//En caso de querer sobreescribir se hace lo mismo. Borra el archivo y lo vuelve a crear pero con el nuevo contenido.
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
    else if(respuesta==4)//Opcion de mostrar la lista de archivos en nuestro microsistema
    {
        listarArchivos();
        limpiarPantalla();
        goto regresa;
    }
    else if(respuesta==0)//con esta opcion entonces ya podemos cerrar el archivo .bin que tenemos abierto.
    {
        printf("Guardando microsistema de archivos y saliendo...\n");
        fclose(pFile);
        return 9;
    }
    return 0;
}
