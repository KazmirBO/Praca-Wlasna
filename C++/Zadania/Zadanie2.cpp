#include <stdio.h>
#include <stdlib.h>

struct p_fizyczny wczytaj(p_fizyczny pracownik, int i, int n);
void wyswietl(p_fizyczny pracownik, int i, int n);
struct p_fizyczny {
  char imie[100], nazwisko[100];
  float l_godzin, stawka, premia;
};

int main(int argc, char *argv[]) {
  int n, i;
  printf("Podaj liczbe pracownikow\n");
  scanf("%d", &n);
  struct p_fizyczny pracownik[n];
  for (i = 0; i < n; i++) {
    pracownik[i] = wczytaj(pracownik[i], i, n);
    wyswietl(pracownik[i], i, n);
  }
  return 0;
}
struct p_fizyczny wczytaj(p_fizyczny pracownik, int i, int n) {
  printf("Podaj imie pracownika nr %d\n", i + 1);
  scanf("%s", pracownik.imie);
  printf("Podaj nazwisko pracownika nr %d\n", i + 1);
  scanf("%s", pracownik.nazwisko);
  printf("Podaj liczbe godzin pracownika nr %d\n", i + 1);
  scanf("%f", &pracownik.l_godzin);
  printf("Podaj stawke pracownika nr %d\n", i + 1);
  scanf("%f", &pracownik.stawka);
  printf("Podaj premie w procentach pracownika nr %d\n", i + 1);
  scanf("%f", &pracownik.premia);
  pracownik.premia = pracownik.stawka * (pracownik.premia * 0.01);
  return pracownik;
}
void wyswietl(p_fizyczny pracownik, int i, int n) {
  printf("Dane pracownika nr %d\n", i + 1);
  printf("Imie: %s\nNazwisko: %s\nLiczba godzin: %5.2f\nStawka: %5.2f\n"
         "Premia: %5.2f\n",
         pracownik.imie, pracownik.nazwisko, pracownik.l_godzin,
         pracownik.stawka, pracownik.premia);
}
