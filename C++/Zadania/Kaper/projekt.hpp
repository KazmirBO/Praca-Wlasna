#ifndef PROJEKT_HPP
#define PROJEKT_HPP
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
using namespace std;
class ule { // Klasa Ule
private:
  string nazwa, rodzaj, uzytkownik;
  int ilosc, identyfikator;

public:
  ule() {
    nazwa = uzytkownik = rodzaj = "";
    ilosc = identyfikator = 0;
  }
  ule(string Nnazwa, string Nrodzaj, string Nuztkownik, int Nilosc,
      int Nident) {
    nazwa = Nnazwa;
    rodzaj = Nrodzaj;
    uzytkownik = Nuztkownik;
    ilosc = Nilosc;
    identyfikator = Nident;
  }
  void wyswietl(string uzyt) {
    if (uzyt == uzytkownik)
      cout << "\nIdentyfikator: " << identyfikator << "\nNazwa: " << nazwa
           << "\nRodzaj: " << rodzaj << "\nIlosc: " << ilosc << endl;
  }
  bool modyfikuj(int ident) {
    if (identyfikator == ident) {
      cout << "Podaj nowa nazwe [stara: " << nazwa << "]: ";
      cin >> nazwa;
      cout << "Podaj nowy rodzaj [stary: " << rodzaj << "]: ";
      cin >> rodzaj;
      cout << "Podaj nowa ilosc [stara: " << ilosc << "]: ";
      cin >> ilosc;
      return 1;
    } else
      return 0;
  }
  string plik() {
    stringstream sIl, sId;
    string sIlosc, sIdent;
    sIl << ilosc;
    sId << identyfikator;
    sIl >> sIlosc;
    sId >> sIdent;
    string tekst = nazwa + ";" + rodzaj + ";" + uzytkownik + ";" + sIlosc +
                   ";" + sIdent + "\n";
    return tekst;
  }
};
class uzytkownicy { // Klasa Użytkownicy
private:
  string nazwa, haslo;

public:
  uzytkownicy() { nazwa = haslo = ""; }
  uzytkownicy(string Nnazwa, string Nhaslo) {
    nazwa = Nnazwa;
    haslo = Nhaslo;
  }
  void wyswietl() { cout << nazwa << endl; }
  bool sprawdz(string Snazwa, string Shaslo) {
    if (Snazwa == nazwa && Shaslo == haslo)
      return 1; // Jeżeli nazwa i hasło użytkownika się zgadza zwraca 1
    else
      return 0; // w innym przypadku 0
  }
};
#endif
