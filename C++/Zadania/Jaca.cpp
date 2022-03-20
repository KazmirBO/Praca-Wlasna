#include <ctime>
#include <iostream>
using namespace std;
class Zamowienie {
private:
  string nazwa_produktu;
  double cena_produktu;
  int liczba_sztuk;
  string data_zakupu = "", tmp = "";

public:
  void zapisz_dane() {
    cout << "Podaj Nazwe: ";
    cin >> nazwa_produktu;
    cout << "Podaj Cene: ";
    cin >> cena_produktu;
    cout << "Podaj Liczbe szt.: ";
    cin >> liczba_sztuk;
    cout << "Podaj Date: " << endl;
    cout << "\tDzien:";
    cin >> tmp;
    data_zakupu += tmp + ".";
    cout << "\tMiesiac:";
    cin >> tmp;
    data_zakupu += tmp + ".";
    cout << "\tRok:";
    cin >> tmp;
    data_zakupu += tmp;
  }
  void wyswietl_dane() {
    cout << "Nazwa: " << nazwa_produktu << endl;
    cout << "Cena: " << cena_produktu << endl;
    cout << "Liczba szt.: " << liczba_sztuk << endl;
    cout << "Data: " << data_zakupu << endl;
  }
  void podaj_nazwe_produktu() { cout << "Nazwa: " << nazwa_produktu << endl; }
  void podaj_cene() { cout << "Cena: " << cena_produktu << endl; }
  void podaj_date_zakupu() { cout << "Data: " << data_zakupu << endl; }
  void podaj_liczbe_sztuk() { cout << "Liczba szt.: " << liczba_sztuk << endl; }
  void podaj_koszt() {
    cout << "Koszta: " << liczba_sztuk * cena_produktu << endl;
  }
};
int main(int argc, char const *argv[]) {
  Zamowienie towar1, towar2;
  int x = 0;
  towar1.zapisz_dane();
  cout << endl;
  towar2.zapisz_dane();
  cout << endl;
  do {
    cout << endl
         << "Menu" << endl
         << "\t1. Wyswietl wszystkie dane." << endl
         << "\t2. Wyswietl nazwe prod." << endl
         << "\t3. Wyswietl cene prod." << endl
         << "\t4. Wyswietl date zakupu." << endl
         << "\t5. Wyswietl liczbe szt." << endl
         << "\t6. Wyswietl koszt cal." << endl
         << "\t7. Koniec" << endl
         << "\tWybierz: ";
    cin >> x;
    switch (x) {
    case 1:
      cout << endl << "Towar 1:" << endl;
      towar1.wyswietl_dane();
      cout << endl << "Towar 2:" << endl;
      towar2.wyswietl_dane();
      break;
    case 2:
      cout << endl << "Towar 1:" << endl;
      towar1.podaj_nazwe_produktu();
      cout << endl << "Towar 2:" << endl;
      towar2.podaj_nazwe_produktu();
      break;
    case 3:
      cout << endl << "Towar 1:" << endl;
      towar1.podaj_cene();
      cout << endl << "Towar 2:" << endl;
      towar2.podaj_cene();
      break;
    case 4:
      cout << endl << "Towar 1:" << endl;
      towar1.podaj_date_zakupu();
      cout << endl << "Towar 2:" << endl;
      towar2.podaj_date_zakupu();
      break;
    case 5:
      cout << endl << "Towar 1:" << endl;
      towar1.podaj_liczbe_sztuk();
      cout << endl << "Towar 2:" << endl;
      towar2.podaj_liczbe_sztuk();
      break;
    case 6:
      cout << endl << "Towar 1:" << endl;
      towar1.podaj_koszt();
      cout << endl << "Towar 2:" << endl;
      towar2.podaj_koszt();
      break;
    }
  } while (x != 7);
  return 0;
}
