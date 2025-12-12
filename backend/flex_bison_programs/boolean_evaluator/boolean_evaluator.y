%{
#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern int yyerror(const char *s);
extern FILE *yyin;

%union {
    int bval; // Boolean value (0 for false, 1 for true)
}

%token <bval> TRUE_KEYWORD FALSE_KEYWORD
%token AND OR NOT LP RP

%right NOT
%left AND
%left OR

%type <bval> expression

%start expression_list

%%

expression_list:
    expression_list expression '\n' { printf("Result: %s\n", $2 ? "true" : "false"); }
    | expression '\n' { printf("Result: %s\n", $1 ? "true" : "false"); }
    ;

expression:
    TRUE_KEYWORD        { $$ = $1; }
    | FALSE_KEYWORD       { $$ = $1; }
    | NOT expression    { $$ = !$2; }
    | expression AND expression { $$ = $1 && $3; }
    | expression OR expression  { $$ = $1 || $3; }
    | LP expression RP  { $$ = $2; }
    ;

%%

int yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
    return 0;
}
