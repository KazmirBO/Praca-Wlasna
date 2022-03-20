#include <iostream>
class Auto {
private:
  std::string producent, kolor;
  double pojemnosc_silnika;

public:
  Auto() {
    producent = "";
    kolor = "";
    pojemnosc_silnika = 0;
  }
  Auto(std::string prod, std::string kol, double poj) {
    producent = prod;
    kolor = kol;
    pojemnosc_silnika = poj;
  }
  double Zwracaj();
  void Wyswietl();
};
double Auto::Zwracaj() { return pojemnosc_silnika; }
void Auto::Wyswietl() {
  std::cout << "Producent: " << producent << std::endl
            << "Kolor: " << kolor << std::endl
            << "Poj. silnika: " << pojemnosc_silnika << std::endl;
}
int main(int argc, char const *argv[]) {
  int n;
  std::string prod, kol;
  double poj, szukane;
  std::cout << "Podaj rozmiar tablicy: ";
  std::cin >> n;
  Auto **tab = (Auto **)malloc(n * sizeof(Auto *));
  for (int i = 0; i < n; i++) {
    std::cout << "Podaj producenta: ";
    std::cin >> prod;
    std::cout << "Podaj kolor: ";
    std::cin >> kol;
    std::cout << "Podaj poj. silnika: ";
    std::cin >> poj;
    tab[i] = new Auto(prod, kol, poj);
  }
  std::cout << "Podaj pojemnosc silnika szukanego auta: ";
  std::cin >> szukane;
  for (int i = 0; i < n; i++) {
    if (tab[i]->Zwracaj() == szukane)
      tab[i]->Wyswietl();
  }
  for (int i = 0; i < n; i++)
    free(tab[i]);
  free(tab);
  return 0;
}
