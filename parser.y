%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);
%}

%union {
    int num;
    char *str;
}

%token <str> ID STRING
%token <num> NUMBER
%token PAPO_QUE CPA CADUCOU BOH MANDA_AE FALA_COMIGO SAI_FORA CONTINUA
%token TRUE FALSE
%token EQ NEQ GE LE GT LT AND OR
%token ATTR PLUS MINUS TIMES DIV MOD
%token LBRACE RBRACE LPAREN RPAREN
%token ERROR

%start programa

%%

programa: LBRACE comandos RBRACE ;

comandos: /* vazio */
        | comandos comando ;

comando:
      declaracao
    | atribuicao
    | condicional
    | loop
    | impressao
    | leitura
    | SAI_FORA
    | CONTINUA
    ;

declaracao: PAPO_QUE ID ATTR expressao ;

atribuicao: ID ATTR expressao ;

condicional: CPA LPAREN expressao RPAREN bloco opt_else ;

opt_else: /* vazio */
        | CADUCOU bloco ;

loop: BOH LPAREN expressao RPAREN bloco ;

impressao: MANDA_AE LPAREN expressao RPAREN ;

leitura: FALA_COMIGO LPAREN RPAREN ;

bloco: LBRACE comandos RBRACE ;

expressao:
      expressao PLUS expressao
    | expressao MINUS expressao
    | expressao TIMES expressao
    | expressao DIV expressao
    | expressao MOD expressao
    | expressao EQ expressao
    | expressao NEQ expressao
    | expressao GE expressao
    | expressao LE expressao
    | expressao GT expressao
    | expressao LT expressao
    | expressao AND expressao
    | expressao OR expressao
    | LPAREN expressao RPAREN
    | NUMBER
    | STRING
    | TRUE
    | FALSE
    | ID
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}
