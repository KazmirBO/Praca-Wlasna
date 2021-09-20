/*
Autor: Sebastian Kolanowski
Temat: Wielomiany
Data:
  Rozpoczecie: 15:30 19-11-2020
  Zakonczenie: xxx
*/
#include <iostream>
#include <cmath>
#include <vector>
//sprawdzenie czy do danego x na pewno wychodzi 0
void wielomian(std::vector<int> wielo,int n,float x){
  float wynik=wielo[0];
  for(int i=1;i<n;i++) wynik=wynik*x+wielo[i];
  std::cout<<"Wartosc wielomianu: "<<wynik<<std::endl;
}
int main(){
  poczatek:
  int i=0;
  //nadanie stopnia wielomianu
  std::cout<<"Podaj stopien wielomianu: ";
  std::cin>>i;
  std::vector<float> dziel;
  std::vector<int> wielo;
  float war;
  for(int j=0;j<=i;j++){
    //testowe - 16x^3-28x^2-4x+3>0
    std::cout<<"Podaj wspolczynnik x"<<i-j<<": ";
    std::cin>>war;
    wielo.push_back(war);
  }
  float pomoc[i+1];
  for(int z=0;z<=i;z++){
    if(wielo[z]<0) pomoc[z]=-wielo[z];
    else pomoc[z]=wielo[z];
  }
  float tmp;
  for(int j=0;j<=i;j++){
    for(int k=0;k<j;k++){
      if(pomoc[j]<pomoc[k]){
        tmp=pomoc[j];
        pomoc[j]=pomoc[k];
        pomoc[k]=tmp;
      }
    }
  }
  float j=0.01, temp=pomoc[i];
  dziel.push_back(0);
  do{
    dziel.push_back(j);
    dziel.push_back(-j);
    j+=0.01;
  }while(j<temp);
  int lop;
  float spraw, mnoz;
  for(int j=0;j<=dziel.size();j++){
    spraw=0; lop=0; mnoz=dziel[j];
    //sprawdzanie dla jakich wartosci x wielomian ma wartosc 0
    for(int pot=i,h=0;h<=i;h++,pot--){
      for(int g=1;g<pot;g++) mnoz*=dziel[j];
      spraw+=wielo[h]*mnoz;
    }
    if(spraw==0){
      //petla do zablokowania powtarzania wartosci x
      for(int y=0;y<j;y++) if(dziel[y]==dziel[j]) lop++;
      //wyswietlenie x
      if(lop==0) std::cout<<"x= "<<dziel[j]<<std::endl;
    }
  }
  float x;
  std::cout<<"Wybiez x: ";
  //wybor wartosci x
  std::cin>>x;
  //sizeof - obliczenie ilosci zmiennych w tablicy
  int n=sizeof(wielo)/sizeof(wielo[0]);
  //wykonanie funkcji
  wielomian(wielo,n,x);
  char tn;
  std::cout<<"Czy chcesz sprobowac jeszcze raz? (T/N): ";
  std::cin>>tn;
  if(tn=='T' || tn=='t'){
    std::cout<<std::endl<<std::endl;
    goto poczatek;
  }
  return 0;
}
