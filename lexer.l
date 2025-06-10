%{
#include "parser.tab.h"
#include <string.h>
%}

digit   [0-9]
letter  [a-zA-Z_]
id      {letter}({letter}|{digit})*

%%

"papo_que"        return PAPO_QUE;
"cpa"             return CPA;
"caducou"         return CADUCOU;
"boh"             return BOH;
"manda_ae"        return MANDA_AE;
"fala_comigo"     return FALA_COMIGO;
"sai_fora"        return SAI_FORA;
"continua"        return CONTINUA;
"fatos"           return TRUE;
"migue"           return FALSE;

"=="              return EQ;
"!="              return NEQ;
">="              return GE;
"<="              return LE;
">"               return GT;
"<"               return LT;
"&&"              return AND;
"||"              return OR;

"="               return ATTR;
"+"               return PLUS;
"-"               return MINUS;
"*"               return TIMES;
"/"               return DIV;
"%"               return MOD;

"{"               return LBRACE;
"}"               return RBRACE;
"("               return LPAREN;
")"               return RPAREN;

\"([^\\\"]|\\.)*\" {
    yylval.str = strdup(yytext);
    return STRING;
}

{id} {
    yylval.str = strdup(yytext);
    return ID;
}

{digit}+ {
    yylval.num = atoi(yytext);
    return NUMBER;
}

"//".*           ;  // ignora comentário

[ \t\r\n]+       ;  // ignora espaços

.                { printf("Caractere inesperado: %s\n", yytext); return ERROR; }

%%

int yywrap(void) { return 1; }
