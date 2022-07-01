#include <iostream>
class Nazwisko {
private:
  char *nazwisko;

public:
  Nazwisko() { nazwisko = ""; }
  Nazwisko(char *nz) {
    nazwisko = nz;
    std::cout << "Nazwisko: " << nazwisko << std::endl;
  }
  ~Nazwisko() { std::cout << "Nazwisko: " << nazwisko << std::endl; }
};
class Pelne : public Nazwisko {
private:
  char *imie;

public:
  Pelne() { imie = ""; }
  Pelne(char *im, char *nz) : Nazwisko(nz) {
    imie = im;
    std::cout << "Imie: " << imie << std::endl;
  }
  ~Pelne() { std::cout << "Imie: " << imie << std::endl; }
};
int main(int argc, char const *argv[]) {
  char *im = "Jacek", *nz = "Bialas";
  Pelne *osoba = new Pelne(im, nz);
  delete osoba;
  return 0;
}
