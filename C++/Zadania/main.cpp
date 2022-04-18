#include <cmath>
#include <iostream>
using namespace std;
float f(float x) {
  return (4 * pow(x, 5)) - (9 * pow(x, 3)) - (16 * pow(x, 2)) + (2 * x) + 4;
}
float zerowe(float a, float b, float przecinek) {
  float srodek = (a + b) / 2;
  while (b - a > przecinek) {
    if (f(a) * f(b) >= 0) {
      cout << "Funkcja nie ma miejsc zerowych." << endl;
      cout << endl;
      exit(1);
    }
    if (f(srodek) == 0) {
      cout << "Miejscem zerowym funkcji jest: " << srodek << "." << endl;
      cout << endl;
      exit(1);
    } else if (f(a) == 0) {
      cout << "Miejscem zerowym funkcji jest: " << a << "." << endl;
      cout << endl;
      exit(1);
    } else if (f(b) == 0) {
      cout << "Miejscem zerowym funkcji jest: " << b << "." << endl;
      cout << endl;
      exit(1);
    }
    if (f(a) * f(srodek) < 0)
      return zerowe(a, srodek, przecinek);
    else
      return zerowe(srodek, b, przecinek);
  }
  cout << "Funkcja nie ma miejsc zerowych." << endl;
  cout << endl;
  exit(1);
}
int main() {
  float a, b, przecinek = 0.001;
  cout << "Podaj a: ";
  cin >> a;
  cout << "Podaj b: ";
  cin >> b;
  cout << "Wynik: " << endl << zerowe(a, b, przecinek);
  cout << endl;
  return 0;
}
