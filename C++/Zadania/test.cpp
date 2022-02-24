#include <fstream>
#include <iostream>

using namespace std;

int main() {
  fstream plik;
  int linijki = 0;
  int slowa = 0;
  int tab[256] = {0};
  plik.open("kordian.txt", ios::in);
  if (plik.good() == true) {
    string ile;
    string napis;
    while (!plik.eof()) {
      getline(plik, napis);
      linijki++;
      if (napis != "\0") {
        slowa++;
      }
      for (int i = 0; i < napis.length(); i++) {
        tab[(int)napis[i]]++;
      }
    }
    fstream plik2;
    plik2.open("wynik.txt", ios::out);
    if (plik2.good() == true) {
      plik2 << linijki << endl;
      plik2 << slowa << endl;
      for (int i = 65; i < 91; i++) {
        if (tab[i] != 0) {
          plik2 << char(i) << " wystepuje " << tab[i] << " razy " << endl;
          cout << char(i) << " wystepuje " << tab[i] << " razy " << endl;
        }
      }
      for (int i = 97; i < 123; i++) {
        if (tab[i] != 0) {
          plik2 << char(i) << " wystepuje " << tab[i] << " razy" << endl;
          cout << char(i) << " wystepuje " << tab[i] << " razy" << endl;
        }
      }
      plik2 << char(32) << " wystepuje " << tab[32] << " razy " << endl;
      cout << char(32) << " wystepuje " << tab[32] << " razy " << endl;
      plik.close();
      plik2.close();
    } else {
      cout << "Blad" << endl;
    }
  }
}
