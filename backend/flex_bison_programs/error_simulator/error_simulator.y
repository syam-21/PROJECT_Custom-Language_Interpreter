%{
#include <stdio.h>
#include <stdlib.h> // For free
#include <string.h> // For strdup

extern int yylex();
extern int yyerror(const char *s);
extern FILE *yyin;

// Simulate errors
void simulate_lexical_error(const char *text) {
    fprintf(stdout, "Simulating Lexical Error:\nInput: %s\nError: Unrecognized token '%s' detected during lexical analysis.\n", text, text);
}

void simulate_syntax_error(const char *text) {
    fprintf(stdout, "Simulating Syntax Error:\nInput: %s\nError: Syntax error near '%s'. Expected different token.\n", text, text);
}

void simulate_semantic_error(const char *text) {
    fprintf(stdout, "Simulating Semantic Error:\nInput: %s\nError: Semantic error: variable '%s' not declared or type mismatch.\n", text, text);
}

void simulate_runtime_error(const char *text) {
    fprintf(stdout, "Simulating Runtime Error:\nInput: %s\nError: Runtime error: division by zero or out of bounds access near '%s'.\n", text, text);
}

%}

%union {
    char *str_val;
}

// Keywords for error types
%token LEXICAL_ERROR_KW SYNTAX_ERROR_KW SEMANTIC_ERROR_KW RUNTIME_ERROR_KW
// Text to simulate error with
%token <str_val> SIM_TEXT

%start program

%%

program:
    /* empty */
    | program error_command
    ;

error_command:
    LEXICAL_ERROR_KW SIM_TEXT { simulate_lexical_error($2); free($2); }
    | SYNTAX_ERROR_KW SIM_TEXT { simulate_syntax_error($2); free($2); }
    | SEMANTIC_ERROR_KW SIM_TEXT { simulate_semantic_error($2); free($2); }
    | RUNTIME_ERROR_KW SIM_TEXT { simulate_runtime_error($2); free($2); }
    ;

%%

int yyerror(const char *s) {
    fprintf(stderr, "PARSER ERROR: %s\n", s);
    return 0;
}

