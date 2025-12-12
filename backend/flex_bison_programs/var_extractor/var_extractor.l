%{
#include "var_extractor.tab.h"
#include <string.h>
%}

%option noyywrap

%%

"char"          { return CHAR; }
"printf"        { return PRINTF; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str_val = strdup(yytext); return IDENTIFIER; }
"[^\"]*"      { yylval.str_val = strdup(yytext); return STRING_LITERAL; }
"[]"            { return BRACKETS; }
"="             { return EQ; }
";"             { return SEMI; }
","             { return COMMA; }
"("             { return LPAREN; }
")"             { return RPAREN; }
[ \t\n\r]+      { /* ignore whitespace */ }
.               { /* ignore other chars */ }

%%