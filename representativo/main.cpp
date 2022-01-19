#include <iostream>
#include <locale>

using std::wcout;
using std::endl;

int main() {

    setlocale( LC_ALL, "" );

    wcout << L"Este é um arquivo de demonstração em C++ compilado pelo RunC" << endl;
    wcout << L"Para adicionar o seu projeto basta acessar Configurações > Projeto e configurar do seu gosto" << endl;
    wcout << L"Para configurar o seu compilador basta acessar Configurações > Compilador e configurar do seu gosto" << endl << endl;
    
    system("pause");
}