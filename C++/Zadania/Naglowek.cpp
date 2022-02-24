#include "Naglowek.hpp"
#include <cmath>
#include <iostream>
using namespace std;
void srodek(struct wspolrzedne A, struct wspolrzedne B) {
  float x = (A.x + B.x) / 2;
  float y = (A.y + B.y) / 2;
  cout << "Srodek wynosi:\n\tx: " << x << "\n\ty: " << y << endl;
}
float odleglosc(struct wspolrzedne A, struct wspolrzedne B) {
  return sqrt(pow(B.x - A.x, 2) + pow(B.y - A.y, 2));
}
