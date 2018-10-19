#include "Nodo.h"

class Pila
{
public:
	int Dato;
	Nodo *Tope,*Base;

	Pila();
	Pila(int Dato);

	bool IsVacio();
	void Push(int Dato);		//Mete
	int Pop();			//Saca
	Nodo* Buscar(int ref);
};