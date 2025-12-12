%{
#include <stdio.h>
#include <stdlib.h> // For strdup
#include <string.h> // For strdup
#include "keyword_identifier.tab.h"
extern YYSTYPE yylval;
%}

%%

"if"        { yylval.str_val = strdup(yytext); return IF; }
"else"      { yylval.str_val = strdup(yytext); return ELSE; }
"while"     { yylval.str_val = strdup(yytext); return WHILE; }
"for"       { yylval.str_val = strdup(yytext); return FOR; }
"int"       { yylval.str_val = strdup(yytext); return INT_TYPE; }
"float"     { yylval.str_val = strdup(yytext); return FLOAT_TYPE; }
"return"    { yylval.str_val = strdup(yytext); return RETURN; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str_val = strdup(yytext); return IDENTIFIER; }
[0-9]+      { yylval.str_val = strdup(yytext); return NUMBER; }
[;(){}]    { /* Ignore punctuation */ }
[ \t\r\n]+    { /* ignore whitespace including newlines */ }
.           { /* Ignore other characters */ }

%%

int yywrap() {
    return 1;
}

