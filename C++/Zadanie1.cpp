#include <iostream>
using namespace std;
struct info_pociag {
  // Deklarujesz strukture pociagow
  int nr_pociagu, czas_op;
  double liczba_km;
};
info_pociag wprowadz(info_pociag pociag); // Kosmetycznie
void drukuj(info_pociag pociag);          // Kosmetycznie
void czy_dop_opoz(info_pociag pociag);    // Kosmetycznie
double wlcowp(info_pociag pociag);        // Kosmetycznie
int main(int argc, char const *argv[]) {
  double laczny_czas = 0;
  // Potem potrzebny do zliczenia sumy opoznien
  int ilosc_poc = 3;
  info_pociag pociagi[ilosc_poc];
  // Deklarujesz tablice struktury pociagow
  for (int i = 0; i < ilosc_poc; i++)
    pociagi[i] = wprowadz(pociagi[i]);
  // Petla do wprowadzania inf o pociagach
  for (int i = 0; i < ilosc_poc; i++)
    drukuj(pociagi[i]);
  // Petla do wyswietlania wszystkich pociagow
  cout << "Dopuszczalny czas opoznienia dla pociagu: " << endl;
  for (int i = 0; i < ilosc_poc; i++)
    czy_dop_opoz(pociagi[i]);
  // Petla do funkcji wyswietlania i sprawdzania, czy pociag sie spoznil
  for (int i = 0; i < ilosc_poc; i++)
    laczny_czas += wlcowp(pociagi[i]);
  // Sumowanie opoznien pociagow
  cout << endl
       << "Laczny czas opoznienia wszystkich pociagow wynosi: " << laczny_czas
       << endl;
  return 0;
}
// info_pociag poniewaz musisz zwrocic element struktury
// Jest poniewaz inaczej nie dzialalo... :D
info_pociag wprowadz(info_pociag pociag) {
  cout << "Podaj numer: ";
  cin >> pociag.nr_pociagu;
  cout << "Podaj Liczbe km: ";
  cin >> pociag.liczba_km;
  cout << "Podaj czas op.: ";
  cin >> pociag.czas_op;
  cout << endl;
  return pociag;
}
// Wyswietlanie wszystkich pociagow
void drukuj(info_pociag pociag) {
  cout << "Nr pociagu: " << pociag.nr_pociagu << endl;
  cout << "Liczba km: " << pociag.liczba_km << endl;
  cout << "Czas op.: " << pociag.czas_op << endl;
  cout << endl;
}
// Sprawdzanie max opoznienia i wyswietlanie
void czy_dop_opoz(info_pociag pociag) {
  double min = (pociag.liczba_km / 70) * 60;
  // KM/70 = ile h jazdy * 60 = min
  cout << "\t" << pociag.nr_pociagu << " wynosi: " << min / 10 << endl;
  if (min / 10 > pociag.czas_op)
    // Jezeli opoznienie < dopuszczalnego opoznienia = zdazyl
    cout << "\tPociag zdazyl na czas." << endl;
  else
    // Jezeli opoznienie > dopuszczalnego opoznienia = nie zdazyl
    cout << "\tPociag nie zdazyl na czas." << endl;
}
// Zwraca wartosc opoznienia kazdego pociagu
double wlcowp(info_pociag pociag) { return pociag.czas_op; }
