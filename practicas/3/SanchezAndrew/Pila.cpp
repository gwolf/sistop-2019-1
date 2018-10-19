#include "Pila.h"

Pila::Pila(){
	this->Tope=NULL;
	this->Base=NULL;
}

Pila::Pila(int dato){
	Nodo *m= new Nodo(dato);
	this->Tope = m;
	this->Base = Tope;
}

bool Pila::IsVacio(){
	return (this->Tope == NULL && this->Base == NULL);
}

void Pila::Push(int dato){
	Nodo *m= new Nodo(dato,this->Tope);
	if (IsVacio())
		this->Base=m;
	this->Tope=m;

	return ;
}


int Pila::Pop(){	
	int d=this->Tope->Dato;
	if (IsVacio())
	{
		std::cout<<"La lista esta vacía."<<std::endl;
		return d;
	}
	Nodo *aux = this->Tope;
	this->Tope=this->Tope->Sig;

	if (this->Tope == NULL)
		this->Base=NULL;

	aux->Sig=NULL;

	return d;
}

Nodo* Pila::Buscar(int ref){
	Nodo *aux = this->Tope;

	if (IsVacio())
	{
		std::cout<<"La lista esta vacía."<<std::endl;
		return NULL;
	}

	while(aux->Dato != ref){
		if(aux->Sig == NULL){
			std::cout<<"La referencia no esta en la lista."<<std::endl;
			return NULL;
		}
		aux=aux->Sig;
	}

	return aux;
}
