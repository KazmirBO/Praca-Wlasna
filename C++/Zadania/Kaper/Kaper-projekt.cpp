#include "projekt.hpp"
#include <cmath>   // Matematyka
#include <ctime>   // Rand
#include <fstream> // Wsparcie dla plików
#include <iostream>
#include <sstream> // String to int
#include <string>  // String
#include <vector>  // Wektory
using namespace std;
int main(int argc, char const *argv[]) {
  srand(time(NULL)); // Rand
  int wybor = 0, menu = 0, uIlosc, ident;
  bool sesja = false, mod = false;
  string nazwa, haslo, uNazwa, uRodzaj, tmp1, tmp2, tekst;
  vector<uzytkownicy> Uzytkownicy; // Wektor klas
  vector<ule> Ule;                 // Wektor klas 2
  fstream plik1, plik2;            // Pliki
  plik1.open("uzytkownicy.txt", ios::in);
  plik2.open("ule.txt", ios::in);
  while (!plik1.eof()) {
    getline(plik1, nazwa, ';'); // Pobieraj tekst do znaku ';'
    getline(plik1, haslo);      // Pobierz resztę tekstu
    if (nazwa != "") {
      // Jeżeli nazwa użytkwnika jest różna od '' dodaj go do klasy
      Uzytkownicy.push_back(uzytkownicy(nazwa, haslo));
    }
  }
  while (!plik2.eof()) {
    stringstream ss1, ss2;
    getline(plik2, uNazwa, ';');  // Pobieraj tekst do znaku ';'
    getline(plik2, uRodzaj, ';'); // w/w
    getline(plik2, nazwa, ';');   // w/w
    getline(plik2, tmp1, ';');    // w/w
    getline(plik2, tmp2);         // Pobierz resztę tekstu
    ss1 << tmp1;
    ss1 >> uIlosc;
    ss2 << tmp2;
    ss2 >> ident;
    if (uNazwa != "") {
      // Jeżeli nazwa ula jest różna od '' dodaj go do klasy
      Ule.push_back(ule(uNazwa, uRodzaj, nazwa, uIlosc, ident));
    }
  }
  nazwa = haslo = ""; // Czyści zawartość nazwy i hasła użytkownika
  while (true) {
    cout << "\n\tMenu:"
            "\n\t1.Logowanie,"
            "\n\t2.Rejestracja,"
            "\n\t3.Wyswietl uzytkownikow,"
            "\n\t4.Wyjdz\n"
            "\n\tWybierz: ";
    cin >> wybor;
    switch (wybor) {
    case 1:
      cout << "\nPodaj nazwe: ";
      cin >> nazwa;
      cout << "Podaj haslo: ";
      cin >> haslo;
      for (int i = 0; i < int(Uzytkownicy.size()); i++) {
        // Sprawdza, czy podane dane są poprawne
        if (Uzytkownicy[i].sprawdz(nazwa, haslo)) {
          system("cls");
          cout << "Zalogowano!" << endl;
          sesja = true;
          break;
        } else
          sesja = false;
      }
      if (sesja) {
        system("cls");
        do {
          cout << "\n\tMenu:"
                  "\n\t1.Wyswietl ule,"
                  "\n\t2.Dodaj ule,"
                  "\n\t3.Modyfikuj ule,"
                  "\n\t4.Wroc do menu glownego.\n"
                  "\n\tWybierz: ";
          cin >> menu;
          switch (menu) {
          case 1:
            system("cls");
            for (int i = 0; i < int(Ule.size()); i++) {
              // Wyświetla wszystkie Pasieki
              Ule[i].wyswietl(nazwa);
            }
            break;
          case 2:
            uNazwa = uRodzaj = "";
            uIlosc = ident = 0;
            cout << "\nPodaj nazwe pasieki: ";
            cin >> uNazwa;
            cout << "Podaj rodzaj uli: ";
            cin >> uRodzaj;
            cout << "Podaj ilosc uli: ";
            cin >> uIlosc;
            // Identyfiaktor = losowa liczba
            ident = rand() % 100000;
            Ule.push_back(ule(uNazwa, uRodzaj, nazwa, uIlosc, ident));
            plik2.close();
            plik2.open("ule.txt", ios::app);
            // Dodaje nowy wpis do pliku
            // np. Sawin;Mieszany;nazwaUzutkownika;10;2137
            plik2 << uNazwa << ";" << uRodzaj << ";" << nazwa << ";" << uIlosc
                  << ";" << ident << endl;
            plik2.close();
            plik2.open("ule.txt", ios::in);
            break;
          case 3:
            ident = 0;
            system("cls");
            for (int i = 0; i < int(Ule.size()); i++) {
              // Wyświetla wszystkie Pasieki
              Ule[i].wyswietl(nazwa);
            }
            cout << "Podaj identyfikator uli, ktory chcesz zmodyfikowac: ";
            cin >> ident;
            plik2.close();
            plik2.open("ule.txt", ios::out);
            for (int i = 0; i < int(Ule.size()); i++) {
              mod = Ule[i].modyfikuj(ident);
              tekst = Ule[i].plik();
              plik2 << tekst;
            }
            tekst = "";
            plik2.close();
            plik2.open("ule.txt", ios::in);
            if (mod) {
              cout << "Zmodyfikowano!" << endl;
              mod = false;
            } else
              cout << "Nie ma takiego ula do modyfikacji!" << endl;
            break;
          case 4:
            sesja = false;
            system("cls");
            break;
          default:
            system("cls");
            cout << "\nZla opcja! Sprobuj ponownie!\n\n";
            break;
          }
        } while (menu != 4);
      } else {
        system("cls");
        cout << "Zle dane! Sprobuj ponownie!" << endl;
      }
      break;
    case 2:
      system("cls");
      plik1.close();
      cout << "Witamy w rejestracji!" << endl;
      cout << "\n\tPodaj nazwe uzytkownika: ";
      cin >> nazwa;
      cout << "\n\tPodaj haslo uzytkownika: ";
      cin >> haslo;
      plik1.open("uzytkownicy.txt", ios::app);
      // Dodaje nowego użytkwnika do pliku
      Uzytkownicy.push_back(uzytkownicy(nazwa, haslo));
      plik1 << nazwa << ";" << haslo << endl;
      system("cls");
      cout << "\tDodano uzytkownika!" << endl;
      plik1.close();
      plik1.open("uzytkownicy.txt", ios::in);
      break;
    case 3:
      system("cls");
      cout << "Lista uzytkownikow:" << endl;
      for (int i = 0; i < int(Uzytkownicy.size()); i++)
        Uzytkownicy[i].wyswietl();
      break;
    case 4:
      // Zamyka pliki
      plik1.close();
      plik2.close();
      return 0;
    default:
      system("cls");
      cout << "\nZla opcja! Sprobuj ponownie!\n\n";
      break;
    }
  }
  // Zamyka pliki
  plik1.close();
  plik2.close();
  return 0;
}
