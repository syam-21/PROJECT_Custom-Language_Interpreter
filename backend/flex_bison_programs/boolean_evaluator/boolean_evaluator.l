#include <stdio.h>
#include "boolean_evaluator.tab.h"
extern YYSTYPE yylval;

%%

"true"          { yylval.bval = 1; return TRUE_KEYWORD; }
"false"         { yylval.bval = 0; return FALSE_KEYWORD; }
"&&"            { return AND; }
"||"            { return OR; }
"!"             { return NOT; }
"("             { return LP; }
")"             { return RP; }
[ 	
]+        { /* ignore whitespace */ }
.               { yyerror("Invalid character"); }

%%

int yywrap() {
    return 1;
}
