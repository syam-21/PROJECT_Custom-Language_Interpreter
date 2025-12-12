%{
#include <stdio.h>
#include <stdlib.h> // For atof, atoi

extern int yylex();
extern int yyerror(const char *s);
extern FILE *yyin;

// Define YYSTYPE using %union
%union {
    float fval;
}

%token <fval> NUMBER
%token ADD SUB MUL DIV LP RP
%right UMINUS

%left ADD SUB
%left MUL DIV

%type <fval> expression

%start expression_list

%%

expression_list:
    expression_list expression '\n' { printf("Result: %f\n", $2); }
    | expression '\n' { printf("Result: %f\n", $1); }
    ;

expression:
    NUMBER
    | expression ADD expression { $$ = $1 + $3; }
    | expression SUB expression { $$ = $1 - $3; }
    | expression MUL expression { $$ = $1 * $3; }
    | expression DIV expression { 
        if ($3 == 0.0) {
            yyerror("Division by zero"); 
            YYABORT;
        }
        $$ = $1 / $3; 
    }
    | LP expression RP { $$ = $2; }
    | SUB expression %prec UMINUS { $$ = -$2; }
    ;    ;

%%

int yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
    return 0;
}
