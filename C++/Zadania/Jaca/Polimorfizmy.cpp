#include <cmath>
#include <iostream>
const double PI = 3.14;
class Bryla {
public:
  Bryla() {}
  virtual ~Bryla() {}
  virtual double objetosc() = 0;
  virtual double pole_po_calk() = 0;
  virtual void pobierz_dane() = 0;
};
class Stozek : public Bryla {
private:
  double r, h, l;
  double objetosc() { return ((PI * pow(r, 2)) * h) / 3; }
  double pole_po_calk() { return PI * r * (r + l); }
  void towrzaca() { l = sqrt(pow(r, 2) + pow(h, 2)); }
  void pobierz_dane() {
    std::cout << "r: ";
    std::cin >> r;
    std::cout << "h: ";
    std::cin >> h;
    towrzaca();
    std::cout << "Objetosc: " << objetosc() << std::endl
              << "Pole: " << pole_po_calk() << std::endl;
  }
};
class Walec : public Bryla {
private:
  double r, h;
  double objetosc() { return PI * pow(r, 2) * h; }
  double pole_po_calk() { return 2 * PI * r * (r + h); }
  void pobierz_dane() {
    std::cout << "r: ";
    std::cin >> r;
    std::cout << "h: ";
    std::cin >> h;
    std::cout << "Objetosc: " << objetosc() << std::endl
              << "Pole: " << pole_po_calk() << std::endl;
  }
};
class Kula : public Bryla {
private:
  double r;
  double objetosc() { return 4 * PI * pow(r, 2); }
  double pole_po_calk() { return 4 * (PI * pow(r, 2)) / 3; }
  void pobierz_dane() {
    std::cout << "r: ";
    std::cin >> r;
    std::cout << "Objetosc: " << objetosc() << std::endl
              << "Pole: " << pole_po_calk() << std::endl;
  }
};
class Czworoscian_foremny : public Bryla {
private:
  double a, h;
  double objetosc() { return (pow(a, 3) * sqrt(2)) / 12; }
  double pole_po_calk() { return pow(a, 2) * sqrt(3); }
  void pobierz_dane() {
    std::cout << "a: ";
    std::cin >> a;
    std::cout << "h: ";
    std::cin >> h;
    std::cout << "Objetosc: " << objetosc() << std::endl
              << "Pole: " << pole_po_calk() << std::endl;
  }
};
class Prostopadloscian : public Bryla {
private:
  double a, b, c;
  double objetosc() { return a * b * c; }
  double pole_po_calk() { return 2 * (a * b + a * c + b * c); }
  void pobierz_dane() {
    std::cout << "a: ";
    std::cin >> a;
    std::cout << "b: ";
    std::cin >> b;
    std::cout << "c: ";
    std::cin >> c;
    std::cout << "Objetosc: " << objetosc() << std::endl
              << "Pole: " << pole_po_calk() << std::endl;
  }
};
void obsluga_bryly(Bryla &b) { b.pobierz_dane(); }
int main(int argc, char const *argv[]) {
  int wybor = 0;
  Bryla *S = new Stozek;
  Stozek s;
  Bryla *W = new Walec;
  Walec w;
  Bryla *K = new Kula;
  Kula k;
  Bryla *C = new Czworoscian_foremny;
  Czworoscian_foremny c;
  Bryla *P = new Prostopadloscian;
  Prostopadloscian p;
  while (wybor != 6) {
    std::cout << "Menu:\n"
              << "\n\t1. Stozek,"
              << "\n\t2. Walec,"
              << "\n\t3. Kula,"
              << "\n\t4. Czworoscian foremny,"
              << "\n\t5. Prostopadloscian,"
              << "\n\t6. Wyjdz."
              << "\n\nWybor: ";
    std::cin >> wybor;
    switch (wybor) {
    case 1:
      std::cout << "Wywolanie polimorficzne: " << std::endl;
      obsluga_bryly(s);
      std::cout << "Wskaznik: " << std::endl;
      S->pobierz_dane();
      break;
    case 2:
      std::cout << "Wywolanie polimorficzne: " << std::endl;
      obsluga_bryly(w);
      std::cout << "Wskaznik: " << std::endl;
      W->pobierz_dane();
      break;
    case 3:
      std::cout << "Wywolanie polimorficzne: " << std::endl;
      obsluga_bryly(k);
      std::cout << "Wskaznik: " << std::endl;
      K->pobierz_dane();
      break;
    case 4:
      std::cout << "Wywolanie polimorficzne: " << std::endl;
      obsluga_bryly(c);
      std::cout << "Wskaznik: " << std::endl;
      C->pobierz_dane();
      break;
    case 5:
      std::cout << "Wywolanie polimorficzne: " << std::endl;
      obsluga_bryly(p);
      std::cout << "Wskaznik: " << std::endl;
      P->pobierz_dane();
      break;
    case 6:
      std::cout << "Wyjscie!" << std::endl;
      break;
    default:
      std::cout << "Zly wybor!" << std::endl;
      break;
    }
  }
  delete S;
  delete W;
  delete K;
  delete C;
  delete P;
  return 0;
}
