#include <iostream>
int main(int argc, char const *argv[]) {
  int tmp, tab[]={4,3,2,1};
  for(int i=0;i<4;i++){
    for(int j=0;j<i;j++){
      if(tab[i]<tab[i+1]){
        tmp=tab[i];
        tab[i]=tab[i+1];
        tab[i+1]=tmp;
      }
    }
  }
  for(auto e:tab) std::cout<<e<<" "<<std::endl;
  return 0;
}
