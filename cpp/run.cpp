#include <iostream>
using namespace std;

int main(){
    system("g++ -I src/include -L src/lib -o main main.cpp -lmingw32 -lSDL2main -lSDL2 -lSDL2_ttf");
    cout<<"Compiled Sucess Fully \n Running...\n";
    system("main.exe");
    cout<<"Ended...";
    return 0;
}
