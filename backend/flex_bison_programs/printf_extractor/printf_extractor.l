%{
#include "printf_extractor.tab.h"
#include <string.h> // For strdup
%}
%option noyywrap
%x PRINTF_ARGS

%%

<INITIAL>"printf"        { return PRINTF; BEGIN PRINTF_ARGS; }
<INITIAL>.|\n            { /* ignore everything else in INITIAL state */ }


<PRINTF_ARGS>"("         { return LPAREN; }
<PRINTF_ARGS>")"         { BEGIN INITIAL; return RPAREN; } // Exit PRINTF_ARGS state
<PRINTF_ARGS>","         { return COMMA; }
<PRINTF_ARGS>"[^"]*"     { yylval.str_val = strdup(yytext); return STRING_LITERAL; }
<PRINTF_ARGS>[a-zA-Z_][a-zA-Z0-9_]* { yylval.str_val = strdup(yytext); return IDENTIFIER; }
<PRINTF_ARGS>[ \t\n]+    { /* ignore whitespace and newlines within args */ }
<PRINTF_ARGS>.          { /* ignore any other character within args */ }

%%
