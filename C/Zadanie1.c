#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct p_fizyczny wczytaj(struct p_fizyczny pracownik, int i, int n);
void wyswietl(struct p_fizyczny pracownik, int i, int n);
float placa(struct p_fizyczny pracownik, int i, float suma);
float najwyzsza(struct p_fizyczny pracownik, float najPlaca);
struct p_fizyczny {
  char imie[100], nazwisko[100];
  float l_godzin, stawka, premia;
};
int main(int argc, char *argv[]) {
  int n, i;
  float suma = 0, najPlaca = 0;
  printf("Podaj liczbe pracownikow\n");
  scanf("%d", &n);

  struct p_fizyczny pracownik[n];
  for (i = 0; i < n; i++) {
    pracownik[i] = wczytaj(pracownik[i], i, n);
    wyswietl(pracownik[i], i, n);
  }
  for (i = 0; i < n; i++)
    suma += placa(pracownik[i], i, suma);
  for (i = 0; i < n; i++)
    najPlaca = najwyzsza(pracownik[i], najPlaca);
  printf("Pracownicy o najwyzszym wynagrodzeniu to:\n");
  for (i = 0; i < n; i++)
    if (pracownik[i].stawka + pracownik[i].premia == najPlaca)
      printf("Imie: %s,\nNazwisko: %s,\nO wynagrodzeniu: %5.2f.\n",
             pracownik[i].imie, pracownik[i].nazwisko,
             pracownik[i].stawka + pracownik[i].premia);
  printf("Sumaryczna kwota wyplat wynosi: %5.2f.\n", suma);

  return 0;
}
struct p_fizyczny wczytaj(struct p_fizyczny pracownik, int i, int n) {
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
void wyswietl(struct p_fizyczny pracownik, int i, int n) {
  printf("Dane pracownika nr %d\n", i + 1);
  printf("Imie: %s\nNazwisko: %s\nLiczba godzin: %5.2f\nStawka: %5.2f\n"
         "Premia: %5.2f\n",
         pracownik.imie, pracownik.nazwisko, pracownik.l_godzin,
         pracownik.stawka, pracownik.premia);
}
float placa(struct p_fizyczny pracownik, int i, float suma) {
  printf("Placa pracownika nr %d wynosi: %5.2f + %5.2f = %5.2f\n", i + 1,
         pracownik.stawka, pracownik.premia,
         pracownik.stawka + pracownik.premia);
  return pracownik.stawka + pracownik.premia;
}
float najwyzsza(struct p_fizyczny pracownik, float najPlaca) {
  if (pracownik.stawka + pracownik.premia > najPlaca)
    najPlaca = pracownik.stawka + pracownik.premia;
  return najPlaca;
}
