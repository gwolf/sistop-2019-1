#include <stdio.h>
#include<stdlib.h>
#include<iostream>
#include<string.h>
#define lonEn 5
//
using namespace std;
void AlfaFnVd(void);
//------------------
int SumaFnEn(int AEn, int BEn){
	return AEn+BEn;
}
int RestaFnEn(int AEn, int BEn){
	return AEn-BEn;
}
int ProductoFnEn(int AEn, int BEn){
	return AEn*BEn;
}
int DivisionFnEn(int AEn,int BEn){
	return AEn/BEn;
}
int (*(*CreaFnApArApFnEn(void))[4])(int,int){
	int(*(*pApArApFnEn)[4])(int, int) = (int(*(*)[4])(int, int))new(int(*[4])(int, int));
	
	(*pApArApFnEn)[0]=SumaFnEn;
	(*pApArApFnEn)[1]=RestaFnEn;
	(*pApArApFnEn)[2]=ProductoFnEn;
	(*pApArApFnEn)[3]=DivisionFnEn;
	
	return pApArApFnEn;
}
//
int (*CreaFnApArEn(void))[4]{
	int(*pApArEn)[4]=(int(*)[4])new int [4];
	int AEn, BEn;
	
	puts("Ingresa un par de enteros");
	cin>>AEn>>BEn;
	
	(*pApArEn)[0]=SumaFnEn(AEn, BEn);
	(*pApArEn)[1]=RestaFnEn(AEn, BEn);
	(*pApArEn)[2]=ProductoFnEn(AEn, BEn);
	(*pApArEn)[3]=DivisionFnEn(AEn, BEn);
	
	return pApArEn;
}
//
main (void){
	int(*(*pApArApFnEn)[4])(int,int)=CreaFnApArApFnEn();
	//p->Ar[4](En1,En2)En3
	for(int iEn=0; iEn<4; iEn++)
	  cout<<(*(*pApArApFnEn)[iEn])(4,4)<<" ";
}

void ExhibeFn(int(*(*pApArApFnEn)[4])(int,int)){
	//cout<< "+-----+\n";
	for(int iEn=0; iEn<4; iEn++)
	//cout<<"/ */->"<<xAr(d[iEn]<<
	cout<<(*(*pApArApFnEn)[iEn])(4,4)<<" ";
}
	
	
