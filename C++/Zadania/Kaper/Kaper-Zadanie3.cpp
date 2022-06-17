#include <fstream>
#include <iostream>
#include <string>
using namespace std;
int main(int argc, char const *argv[]) {
  string tmp;
  int n = 0, i = 0;
  std::ifstream plik("./dane.dat");
  while (!plik.eof()) {
    getline(plik, tmp);
    n++;
  }
  plik.close();
  float *liczby = (float *)calloc(n, sizeof(float));
  std::ifstream plik2("./dane.dat");
  while (!plik2.eof()) {
    getline(plik2, tmp);
    liczby[i] = stof(tmp);
    i++;
  }
  plik2.close();
  return 0;
}
