#include <stdio.h>

int yyparse(void);

int main() {
    printf("Iniciando BarScript...\n");
    return yyparse();
}
