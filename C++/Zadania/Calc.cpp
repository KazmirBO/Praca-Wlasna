// Kalkulator dodający 2 liczby o rozmiarze PONAD 50 znaków
#include <iostream>
int main(int argc, char const *argv[]) {
  double liczba1, liczba2;
  std::cin >> liczba1;
  std::cin >> liczba2;
  std::cout << liczba1 + liczba2 << std::endl;
  return 0;
}
