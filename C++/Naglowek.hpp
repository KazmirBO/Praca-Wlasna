#ifndef NAGLOWEK_H
#define NAGLOWEK_H
struct wspolrzedne {
  int x;
  int y;
};
void srodek(struct wspolrzedne A, struct wspolrzedne B);
float odleglosc(struct wspolrzedne A, struct wspolrzedne B);
#endif
