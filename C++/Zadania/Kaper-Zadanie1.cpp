#include <cmath>
#include <iostream>
using namespace std;
int main(int argc, char const *argv[]) {
  float t[6][6], suma = 0;
  int w, k;
  for (int i = 0; i < 6; i++)
    for (int j = 0; j < 6; j++)
      t[i][j] = pow(-1.0, i - j);
  cout << "Podaj wiersz:";
  cin >> w;
  cout << "Podaj kolumne:";
  cin >> k;
  for (int i = 0; i < 6; i++)
    suma += t[w][i];
  for (int i = 0; i < 6; i++)
    suma += t[i][k];
  cout << "Suma wynosi:" << suma << endl;
  return 0;
}
