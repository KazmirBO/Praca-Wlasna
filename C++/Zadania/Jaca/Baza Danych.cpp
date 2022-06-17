#include <iostream>
using namespace std;
class Urzadzenia {
protected:
  string firma;
  int obroty;

public:
  Urzadzenia() {
    firma = "";
    obroty = 0;
  }
  Urzadzenia(string f, int o) {
    firma = f;
    obroty = o;
  }
  string daj_firme() { return firma; }
  int daj_obroty() { return obroty; }
  void pokaz_opis() { cout << daj_firme() << endl << daj_obroty() << endl; }
};
class SzlifierkaKatowa : public Urzadzenia {
private:
  int moc;
  int tarcza;

public:
  SzlifierkaKatowa() : Urzadzenia() { moc = tarcza = 0; }
  SzlifierkaKatowa(int m, int t, string f, int o) : Urzadzenia(f, o) {
    moc = m;
    tarcza = t;
  }
  int daj_moc() { return moc; }
  int daj_tarcze() { return tarcza; }
  void pokaz_opis() {
    cout << daj_moc() << endl << daj_tarcze() << endl;
    Urzadzenia::pokaz_opis();
  }
};
class WiertarkoWkretarka : public Urzadzenia {
private:
  double napiecie;
  string bateria;
  int czas_ladow;

public:
  WiertarkoWkretarka() : Urzadzenia() {
    napiecie = 0;
    bateria = "";
    czas_ladow = 0;
  }
  WiertarkoWkretarka(double n, string b, int c, string f, int o)
      : Urzadzenia(f, o) {
    napiecie = n;
    bateria = b;
    czas_ladow = c;
  }
  double daj_napiecie() { return napiecie; }
  string daj_baterie() { return bateria; }
  int daj_czas() { return czas_ladow; }
  void pokaz_opis() {
    cout << daj_napiecie() << endl
         << daj_baterie() << endl
         << daj_czas() << endl;
    Urzadzenia::pokaz_opis();
  }
};
void Obroty(SzlifierkaKatowa sk[], int rozmiar) {
  SzlifierkaKatowa obroty = sk[0];
  for (int i = 1; i < rozmiar; i++) {
    if (obroty.daj_obroty() < sk[i].daj_obroty())
      obroty = sk[i];
  }
  obroty.pokaz_opis();
}
void Ladowanie(WiertarkoWkretarka ww[], int rozmiar) {
  WiertarkoWkretarka ladowanie = ww[0];
  for (int i = 1; i < rozmiar; i++) {
    if (ladowanie.daj_czas() > ww[i].daj_czas())
      ladowanie = ww[i];
  }
  ladowanie.pokaz_opis();
}
int main(int argc, char const *argv[]) {
  int rozsk = 2, rozww = 2;
  SzlifierkaKatowa sk[rozsk] = {SzlifierkaKatowa(50, 30, "KWZ", 3000),
                                SzlifierkaKatowa(100, 60, "BPP", 10000)};
  WiertarkoWkretarka ww[rozww]{
      WiertarkoWkretarka(12.6, "900mAh", 4, "PHILIPS", 12000),
      WiertarkoWkretarka(14.4, "BRAK", 0, "NO-NAME", 10000)};
  Obroty(sk, rozsk);
  Ladowanie(ww, rozww);
  return 0;
}
