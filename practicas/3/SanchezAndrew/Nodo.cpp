#include "Nodo.h"


Nodo::Nodo(int Dato,Nodo *Sig){
	this->Dato=Dato;
	this->Sig=Sig;
}

Nodo::Nodo(int Dato){
	this->Dato=Dato;
	this->Sig=NULL;
}