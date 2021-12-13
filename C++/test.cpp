/*
Autor: Kolanowski Sebastian
Projekt: Kolokwium - Zadanie 1
Data 14.12.2020
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(){
  int x1,y1,x2,y2,przy1=0,przy2=0;
  float prze;
  float PI=3.14;
  char tn; //2277
  printf("Podaj 4 liczby: \n");
  printf("\tx1= "); scanf("%d",&x1);
  printf("\ty1= "); scanf("%d",&y1);
  printf("\tx2= "); scanf("%d",&x2);
  printf("\ty2= "); scanf("%d",&y2);
  printf("Twoje liczby to: A=(%2d,%2d), B=(%2d,%2d).\n",x1,y1,x2,y2);
  if(x1>x2){
    przy1=x1-x2;
  }
  if(x1<x2){
    przy1=x2-x1;
  }
  if(y1>y2){
    przy2=y1-y2;
  }
  if(y1<y2){
    przy2=y2-y1;
  }
  prze=(przy1*przy1)+(przy2*przy2);
  prze=sqrt(prze);
  float r=prze/2;
  int wybor;
  printf("\nCo chesz zrobiæ:\n\t1-Wyznacz obw\n\t2-Wyznacz pole\n\t3-Koniec programu\n");
  do{
    printf("\n\tWyberz: ");
    scanf("%d",&wybor);
    switch(wybor){
      case 1:
        printf("\tObw kola wynosi: %f.\n",2*PI*r);
        break;
      case 2:
        printf("\tPole kola wynosi: %f.\n",PI*(r*r));
        break;
      case 3:
          return 0;
        break;
      default:
        printf("\tWybrales zla liczbe!\n");
        break;
    }
  }while(wybor!=3);
  return 0;
}
