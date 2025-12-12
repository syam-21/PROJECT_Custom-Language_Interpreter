%{ 
#include <stdio.h>
#include <math.h> // For NAN
#include <stdlib.h> // For exit

extern int yylex();
extern void yyerror(const char *s); // Corrected declaration as void
// extern double yylval; // Removed conflicting declaration

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

extern FILE *yyin;
extern void yyrestart(FILE *input_file);
%}

%token <val> NUMBER
%token ADD SUB MUL DIV
%token LPAREN RPAREN
%token EOL
%token EXIT_CMD

%type <val> expr

%union {
    double val;
}

// Operator precedence and associativity
%left ADD SUB
%left MUL DIV

%%

program:
    program line
    | /* empty */
;

line:
    expr EOL        { printf("= %f\n", $1); }
    | EXIT_CMD EOL  { printf("Exiting...\n"); YYACCEPT; } // YYACCEPT exits the parser
    | EOL           { /* empty line, do nothing */ }
    | error EOL     { yyclearin; yyerrok; printf("Error: Invalid expression\n"); }
;

expr:
    NUMBER               { $$ = $1; }
    | expr ADD expr      { $$ = $1 + $3; }
    | expr SUB expr      { $$ = $1 - $3; }
    | expr MUL expr      { $$ = $1 * $3; }
    | expr DIV expr      {
        if ($3 == 0.0) {
            yyerror("Division by zero");
            $$ = NAN; // Not a Number
            YYABORT; // Abort parsing for this line
        }
        $$ = $1 / $3;
    }
    | LPAREN expr RPAREN { $$ = $2; }
;

%%

int main(void) {
    yyin = stdin; // Set input to stdin
    yyparse();
    return 0;
}