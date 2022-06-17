#include <fstream>
#include <iostream>
#include <string>
using namespace std;
class Sprzet {
private:
  int identyfikator;
  string typ;

public:
  Sprzet() {
    identyfikator = 0;
    typ = "";
  }
  Sprzet(int ident, string t) {
    identyfikator = ident;
    typ = t;
  }
  void Zwroc(fstream &plik) { plik << identyfikator << ";" << typ << endl; }
  string Udostepnij() { return typ; }
};
class Osoba {
private:
  int identyfikator, wiek;
  string nazwisko;

public:
  Osoba() {
    identyfikator = wiek = 0;
    nazwisko = "";
  }
  Osoba(int ident, int w, string naz) {
    identyfikator = ident;
    wiek = w;
    nazwisko = naz;
  }
  void Zwroc(fstream &plik) {
    plik << identyfikator << ";" << wiek << ";" << nazwisko << endl;
  }
  int Udostepnij() { return wiek; }
  void Wyswietl() {
    cout << "Nazwisko: " << nazwisko << endl << "Wiek: " << wiek << endl;
  }
};
class Wypozyczenie {
private:
  int identyfikator_sprzetu, identyfikator_osoby;

public:
  Wypozyczenie() { identyfikator_osoby = identyfikator_sprzetu = 0; }
  Wypozyczenie(int identO, int identS) {
    identyfikator_osoby = identO;
    identyfikator_sprzetu = identS;
  }
  void Zwroc(fstream &plik) {
    plik << identyfikator_osoby << ";" << identyfikator_sprzetu << endl;
  }
  int Osoba() { return identyfikator_osoby; }
  int Sprzet() { return identyfikator_sprzetu; }
};
void Hulajnogi(Sprzet spr[], Osoba oso[], Wypozyczenie wyp[]) {
  for (int i = 0; i < 3; i++) {
    if (spr[wyp[i].Sprzet() - 1].Udostepnij() == "hulajnoga" &&
        oso[wyp[i].Osoba() - 1].Udostepnij() > 25)
      oso[i].Wyswietl();
  }
}
int Rowery(Sprzet spr[], Wypozyczenie wyp[]) {
  int ilosc = 0;
  for (int i = 0; i < 3; i++) {
    if (spr[wyp[i].Sprzet() - 1].Udostepnij() == "rower")
      ilosc++;
  }
  return ilosc;
}
int main(int argc, char const *argv[]) {
  int is, io, iw, tmp1, tmp2;
  string tmps;
  Sprzet spr[3] = {Sprzet(1, "rower"), Sprzet(2, "hulajnoga"),
                   Sprzet(3, "rolki")};
  Osoba oso[3] = {Osoba(1, 26, "Kowal"), Osoba(2, 12, "Malina"),
                  Osoba(3, 33, "Nowik")};
  Wypozyczenie wyp[3] = {Wypozyczenie(1, 1), Wypozyczenie(2, 1),
                         Wypozyczenie(3, 2)};
  is = io = iw = 0;
  fstream plik1, plik2, plik3;
  plik1.open("Sprzet.txt", ios::out);
  plik2.open("Osoba.txt", ios::out);
  plik3.open("Wypozyczenie.txt", ios::out);
  for (auto e : spr) {
    e.Zwroc(plik1);
  }
  for (auto e : oso) {
    e.Zwroc(plik2);
  }
  for (auto e : wyp) {
    e.Zwroc(plik3);
  }
  plik1.close();
  plik2.close();
  plik3.close();
  plik1.open("Sprzet.txt", ios::in);
  plik2.open("Osoba.txt", ios::in);
  plik3.open("Wypozyczenie.txt", ios::in);
  while (!plik1.eof()) {
    getline(plik1, tmps, ';');
    if (tmps != "") {
      tmp1 = stoi(tmps);
      getline(plik1, tmps);
      spr[is] = Sprzet(tmp1, tmps);
      is++;
    }
  }
  while (!plik2.eof()) {
    getline(plik2, tmps, ';');
    if (tmps != "") {
      tmp1 = stoi(tmps);
      getline(plik2, tmps, ';');
      tmp2 = stoi(tmps);
      getline(plik2, tmps);
      oso[io] = Osoba(tmp1, tmp2, tmps);
      io++;
    }
  }
  while (!plik3.eof()) {
    getline(plik3, tmps, ';');
    if (tmps != "") {
      tmp1 = stoi(tmps);
      getline(plik3, tmps);
      tmp2 = stoi(tmps);
      wyp[iw] = Wypozyczenie(tmp1, tmp2);
      iw++;
    }
  }
  cout << "Osoby, ktore maja ponad 25 lat i wypozyczyly hulajnogi to: " << endl;
  Hulajnogi(spr, oso, wyp);
  cout << "Ilosc wypozyczonych rowerow wynosi: " << Rowery(spr, wyp) << endl;
  return 0;
}
