#include "Naglowek.cpp"
#include "Naglowek.hpp"
#include <cstdlib>
#include <iostream>

using namespace std;

int main() {
  struct wspolrzedne A, B;
  int x = 0;
  cout << "Podaj A.x: ";
  cin >> A.x;
  cout << "Podaj A.y: ";
  cin >> A.y;
  cout << "Podaj B.x: ";
  cin >> B.x;
  cout << "Podaj B.y: ";
  cin >> B.y;
  while (true) {
    cout << "\t\t***MENU***\n"
         << "\t1.Współrzędne środka odcinka |AB|\n"
         << "\t2.Sumę odległości odcinków |OC|, |AC| oraz |CB|\n"
         << "\t3.Koniec\n\n"
         << "\tWybieram : ";
    cin >> x;

    switch (x) {
    case 1:
      srodek(A, B);
      break;
    case 2:
      cout << "Odleglosc miedzy punktami wynosi: " << odleglosc(A, B) << endl;
      break;
    case 3:
      return 0;
      break;
    default:
      cout << "Zly wybor!" << endl;
      break;
    }
  }
  return 0;
}
