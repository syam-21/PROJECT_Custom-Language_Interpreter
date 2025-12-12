%{
#include <iostream>
#include <string>
#include <vector>
#include <stdio.h>

extern int yylex();
extern FILE* yyin;
void yyerror(const char *s);

%}

%union {
    char *str_val;
}

%token PRINTF
%token LPAREN RPAREN COMMA
%token <str_val> STRING_LITERAL IDENTIFIER

%start program

%%

program:
    /* empty */
    | program printf_statement
    ;

printf_statement:
    PRINTF LPAREN STRING_LITERAL COMMA arg_list RPAREN {
        std::string format_str = $3;
        printf("Format string: %s\n", format_str.substr(1, format_str.length() - 2).c_str());
        free($3);
    }
    | PRINTF LPAREN STRING_LITERAL RPAREN {
        std::string format_str = $3;
        printf("Format string: %s\n", format_str.substr(1, format_str.length() - 2).c_str());
        free($3);
    }
    ;

arg_list:
    IDENTIFIER { printf("Argument: %s\n", $1); free($1); }
    | arg_list COMMA IDENTIFIER { printf("Argument: %s\n", $3); free($3); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Parser error: %s\n", s);
}

int main(void) {
    extern FILE *yyin;
    yyin = fopen("test_code.c", "r");
    if (!yyin) {
        perror("Error opening test_code.c");
        return 1;
    }
    
    yyparse();
    
    fclose(yyin);
    return 0;
}