/*
Autor: Sebastian Kolanowski
Temat: Wielomiany
Data:
  Rozpoczecie: 15:30 19-11-2020
  Zakonczenie: ???
*/
#include <iostream>
#include <cmath>
struct ulamek{
  float l,m;
};
using namespace std;
void wielomian(int wielo[],int n,int x);
void wspolczynnik(int wielo[],int i);
//void liczenie();
int main(){
  poczatek:
  int stopien=0,temp=1;
  cout<<"Podaj stopien wielomianu: ";
  cin>>stopien;
  //nadanie stopnia wielomianu
  int dziel[1000],wielo[stopien+1];
  wspolczynnik(wielo,stopien);
  int pomoc[stopien+1];
  for(int i=0;i<=stopien;i++){
    if(wielo[i]<0){
      pomoc[i]=wielo[i]*-1;
    }
    else{
      pomoc[i]=wielo[i];
    }
    for(int j=1;j<=pomoc[i];j++){
      //sprawdzanie dzielnikow
	     if(pomoc[i]%j==0){
         dziel[0]=0;
         //ewentualne zabezpieczenie z 0 - male problemy
         dziel[temp]=j;
         //cout << dziel[temp] << endl;
         temp++;
         dziel[temp]=(-j);
         //cout << dziel[temp] << endl;
         temp++;
       }
    }
  }
  int lop,spraw;
  for(int j=0;j<=temp;j++){
    spraw=0;
    lop=0;
    for(int pot=stopien,h=0;h<=stopien;h++,pot--){
      //sprawdzanie dla jakich wartosci x wielomian ma wartosc 0
      spraw=spraw+wielo[h]*pow(dziel[j],pot);
    }
    if(spraw==0){
      for(int y=0;y<j;y++){
        //petla do zablokowania powtarzania wartosci x
        if(dziel[y]==dziel[j]){
          lop++;
        }
      }
      if(lop==0){
        //wyswietlenie x
        cout<<"\tx= "<<dziel[j]<<endl;
      }
    }
  }
  int x;
  cout<<"Wybiez x: ";
  cin>>x;
  //wybor wartosci x
  int n=sizeof(wielo)/sizeof(wielo[0]);
  //sizeof - obliczenie ilosci zmiennych w tablicy
  wielomian(wielo,n,x);
  //wykonanie funkcji
  char tn;
  cout<<"Czy chcesz sprobowac jeszcze raz? (T/N): ";
  cin>>tn;
  if(tn=='T' || tn=='t'){
    cout<<endl<<endl;
    goto poczatek;
  }
  return 0;
}
void wielomian(int wielo[],int n,int x){
  //sprawdzenie czy do danego x na pewno wychodzi 0
  int wynik=wielo[0];
  for(int i=1;i<n;i++){
    wynik=wynik*x+wielo[i];
  }
  cout<<"Wartosc wielomianu: "<<wynik<<endl;
}
void wspolczynnik(int wielo[], int i){
  for(int j=0;j<=i;j++){
    cout<<"Podaj wspolczynnik x"<<i-j<<": ";
    cin>>wielo[j];
  }
}
