%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h> // For strdup
#include "error_simulator.tab.h"
extern YYSTYPE yylval;

// Global variable to store input for error simulation
char *sim_input = NULL;

%}

%option noyywrap

%%

"lexical_error"     { return LEXICAL_ERROR_KW; }
"syntax_error"      { return SYNTAX_ERROR_KW; }
"semantic_error"    { return SEMANTIC_ERROR_KW; }
"runtime_error"     { return RUNTIME_ERROR_KW; }

"(\\.|[^"\\])*" { yylval.str_val = strdup(yytext); return SIM_TEXT; }

[ \t\r\n]+      { /* Ignore whitespace and newlines */ }

.               { fprintf(stderr, "LEXICAL ERROR: Unrecognized character in simulator command: %s\n", yytext); }

%%
