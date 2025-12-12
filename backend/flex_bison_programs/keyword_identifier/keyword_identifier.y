%{
#include <stdio.h>
#include <stdlib.h>
#include <set>
#include <string>
#include <vector>

extern int yylex();
extern FILE* yyin;
void yyerror(const char *s);

std::set<std::string> extractedKeywords;
std::set<std::string> extractedIdentifiers;

%}

%union {
    char *str_val;
}

%token <str_val> IF ELSE WHILE FOR INT_TYPE FLOAT_TYPE RETURN IDENTIFIER NUMBER

%start program

%%

program:
    /* empty */
    | program token
    ;
token:
    IF          { extractedKeywords.insert(std::string($1)); free($1); }
    | ELSE      { extractedKeywords.insert(std::string($1)); free($1); }
    | WHILE     { extractedKeywords.insert(std::string($1)); free($1); }
    | FOR       { extractedKeywords.insert(std::string($1)); free($1); }
    | INT_TYPE  { extractedKeywords.insert(std::string($1)); free($1); }
    | FLOAT_TYPE { extractedKeywords.insert(std::string($1)); free($1); }
    | RETURN    { extractedKeywords.insert(std::string($1)); free($1); }
    | IDENTIFIER { extractedIdentifiers.insert(std::string($1)); free($1); }
    | NUMBER    { free($1); }
    ;

%%

int main(void) {
    yyin = stdin;
    do {
        yyparse();
    } while (!feof(yyin));

    printf("Keywords:\n");
    for (std::set<std::string>::iterator it = extractedKeywords.begin(); it != extractedKeywords.end(); ++it) {
        printf("%s\n", (*it).c_str());
    }

    printf("\nIdentifiers:\n");
    for (std::set<std::string>::iterator it = extractedIdentifiers.begin(); it != extractedIdentifiers.end(); ++it) {
        printf("%s\n", (*it).c_str());
    }
    
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Parser Error: %s\n", s);
}
