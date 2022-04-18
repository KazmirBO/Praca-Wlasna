#include <iostream>
class Silnik {
private:
  int pojemnosc;
  std::string producent;

public:
  void nadaj(int poj, std::string prod) {
    pojemnosc = poj;
    producent = prod;
  }
  std::string zwroc() { return producent; }
  void przekaz() {
    std::cout << "Pojemnosc: " << pojemnosc << std::endl
              << "Producent silnika: " << producent << std::endl;
  }
};
class Urzadzenie {
private:
  std::string producent;
  int obroty;
  Silnik silnik;

public:
  Urzadzenie(std::string prod, int obr, int poj, std::string sProd) {
    producent = prod;
    obroty = obr;
    silnik.nadaj(poj, sProd);
  }
  bool sprawdz() {
    if (producent == silnik.zwroc())
      return 1;
    else
      return 0;
  }
  void przekaz() {
    std::cout << "Producent: " << producent << std::endl
              << "Obroty: " << obroty << std::endl;
    silnik.przekaz();
  }
};

void wyswietl(Urzadzenie tab[]) {
  for (int i = 0; i < 6; i++) {
    if (tab[i].sprawdz() == true)
      tab[i].przekaz();
  }
}
int main(int argc, char const *argv[]) {
  Urzadzenie tab[] = {
      {"Audi", 3000, 3, "Renault"},    {"Opel", 2000, 1, "BMW"},
      {"Renault", 3000, 2, "Peugeot"}, {"Peugeot", 1000, 3, "Peugeot"},
      {"BMW", 2000, 3, "BMW"},         {"Opel", 2500, 2, "Opel"}};
  wyswietl(tab);
  return 0;
}
