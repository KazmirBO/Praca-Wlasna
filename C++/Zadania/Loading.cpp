#include <ctime>
#include <iostream>
#include <unistd.h>
int main(int argc, char const *argv[]) {
  system("clear");
  srand(time(NULL));
  std::string loading = "";
  for (int i = 0; i < 80; i += rand() % 10) {
    if (i < 80) {
      for (int j = 0; j < i; j++) {
        loading += "=";
      }
      std::cout << loading << ">" << std::endl;
    } else {
      for (int j = 0; j < i; j++) {
        loading += "=";
      }
      std::cout << loading << ">" << std::endl;
    }
    sleep(1);
    system("clear");
    loading = "";
  }
  return 0;
}
