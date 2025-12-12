%{
#include <stdio.h>
#include "calculator.tab.h"
extern YYSTYPE yylval;
%}

%%

([0-9]+(\.[0-9]*)?|\.[0-9]+) { yylval.fval = atof(yytext); return NUMBER; }
"+"             { return ADD; }
"-"             { return SUB; }
"*"             { return MUL; }
"/"             { return DIV; }
"("             { return LP; }
")"             { return RP; }
[ \t\n]+        { /* ignore whitespace */ }
.               { yyerror("Invalid character"); }

%%

int yywrap() {
    return 1;
}
