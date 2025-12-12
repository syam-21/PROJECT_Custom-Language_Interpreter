/* C++ headers and declarations */
%{ 
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stdio.h>

extern int yylex();
extern FILE* yyin;
void yyerror(const char *s);

// Global data structures to hold extracted info
std::map<std::string, std::string> variables;
std::vector<std::string> print_order;

%}

/* Bison declarations */
%union {
    char *str_val;
}

%token CHAR PRINTF BRACKETS EQ SEMI COMMA LPAREN RPAREN
%token <str_val> IDENTIFIER
%token <str_val> STRING_LITERAL

%start program

%%

program:
    /* empty */
    | program statement
    ;

statement:
    declaration
    | print_statement
    ;

declaration:
    CHAR IDENTIFIER BRACKETS EQ STRING_LITERAL SEMI {
        std::string var_name = $2;
        std::string var_value = $5;
        variables[var_name] = var_value.substr(1, var_value.length() - 2);
        free($2);
        free($5);
    }
    ;

print_statement:
    // Match: printf("...", identifier, identifier, ...);
    PRINTF LPAREN STRING_LITERAL COMMA identifier_list RPAREN SEMI {
        free($3); // Free the format string literal
    }
    ;

identifier_list:
    IDENTIFIER { print_order.push_back($1); free($1); }
    | identifier_list COMMA IDENTIFIER { print_order.push_back($3); free($3); }
    ;

%%

void yyerror(const char *s) {
    /* Suppress errors */
}

int main(void) {
    yyin = stdin;
    yyparse();
    
    // Print JSON output
    printf("{\n");
    printf("  \"variables\": {\n");
    for (auto it = variables.begin(); it != variables.end(); ++it) {
        printf("    \"%s\": \"%s\"%s\n", it->first.c_str(), it->second.c_str(),
               std::next(it) == variables.end() ? "" : ",");
    }
    printf("  },\n");
    printf("  \"print_order\": [\n");
    for (auto it = print_order.begin(); it != print_order.end(); ++it) {
        printf("    \"%s\"%s\n", it->c_str(),
               std::next(it) == print_order.end() ? "" : ",");
    }
    printf("  ]\n");
    printf("}\n");
    
    return 0;
}