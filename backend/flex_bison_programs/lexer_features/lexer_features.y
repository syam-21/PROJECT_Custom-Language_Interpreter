%{
#include <stdio.h>
#include <stdlib.h>
#include <set>
#include <string>
#include <iostream>

extern int yylex();
extern FILE* yyin;
void yyerror(const char *s);

// Sets to store unique tokens
std::set<std::string> keywords;
std::set<std::string> identifiers;
std::set<std::string> operators;
std::set<std::string> delimiters;
std::set<std::string> stringLiterals; // New set for string literals

%}

// Define the union for token values
%union {
    char *str_val;
    float float_val; // Kept for compatibility with the lexer, though not used for output
}

// Declare all tokens from the lexer
// The <str_val> is only needed for tokens that carry a string value (like IDENTIFIER)
%token IF_KW ELSE_KW WHILE_KW FOR_KW RETURN_KW TYPE_INT TYPE_FLOAT TYPE_STRING
%token <str_val> IDENTIFIER
%token <float_val> NUMBER
%token <str_val> STRING_LITERAL
%token OP_PLUS OP_MINUS OP_MUL OP_DIV OP_ASSIGN OP_EQ OP_NE OP_LT OP_GT OP_LE OP_GE OP_AND OP_OR OP_NOT
%token DEL_LP DEL_RP DEL_LC DEL_RC DEL_LB DEL_RB DEL_SEMICOLON DEL_COMMA DEL_DOT

%start program

%%

program:
    /* empty */
    | program token
    ;

token:
    IF_KW { keywords.insert("if"); }
    | ELSE_KW { keywords.insert("else"); }
    | WHILE_KW { keywords.insert("while"); }
    | FOR_KW { keywords.insert("for"); }
    | RETURN_KW { keywords.insert("return"); }
    | TYPE_INT { keywords.insert("int"); }
    | TYPE_FLOAT { keywords.insert("float"); }
    | TYPE_STRING { keywords.insert("string"); }
    | IDENTIFIER { identifiers.insert(std::string($1)); free($1); }
    | NUMBER { /* Ignore numbers as per request */ }
    | STRING_LITERAL { stringLiterals.insert(std::string($1)); free($1); } // Collect string literals
    | OP_PLUS { operators.insert("+"); }
    | OP_MINUS { operators.insert("-"); }
    | OP_MUL { operators.insert("*"); }
    | OP_DIV { operators.insert("/"); }
    | OP_ASSIGN { operators.insert("="); }
    | OP_EQ { operators.insert("=="); }
    | OP_NE { operators.insert("!="); }
    | OP_LT { operators.insert("<"); }
    | OP_GT { operators.insert(">"); }
    | OP_LE { operators.insert("<="); }
    | OP_GE { operators.insert(">="); }
    | OP_AND { operators.insert("&&"); }
    | OP_OR { operators.insert("||"); }
    | OP_NOT { operators.insert("!"); }
    | DEL_LP { delimiters.insert("("); }
    | DEL_RP { delimiters.insert(")"); }
    | DEL_LC { delimiters.insert("{"); }
    | DEL_RC { delimiters.insert("}"); }
    | DEL_LB { delimiters.insert("["); }
    | DEL_RB { delimiters.insert("]"); }
    | DEL_SEMICOLON { delimiters.insert(";"); }
    | DEL_COMMA { delimiters.insert(","); }
    | DEL_DOT { delimiters.insert("."); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "PARSER ERROR: %s\n", s);
}

int main(void) {
    yyin = stdin;
    do {
        yyparse();
    } while (!feof(yyin));

    printf("- Keywords: ");
    for (auto it = keywords.begin(); it != keywords.end(); ++it) {
        printf("%s%s", it->c_str(), std::next(it) == keywords.end() ? "" : ", ");
    }

    printf("\n- Identifiers: ");
    for (auto it = identifiers.begin(); it != identifiers.end(); ++it) {
        printf("%s%s", it->c_str(), std::next(it) == identifiers.end() ? "" : ", ");
    }

    printf("\n- Operators: ");
    for (auto it = operators.begin(); it != operators.end(); ++it) {
        printf("%s%s", it->c_str(), std::next(it) == operators.end() ? "" : ", ");
    }

    printf("\n- Delimiters: ");
    for (auto it = delimiters.begin(); it != delimiters.end(); ++it) {
        printf("%s%s", it->c_str(), std::next(it) == delimiters.end() ? "" : ", ");
    }
    
    printf("\n- String Literals: ");
    for (auto it = stringLiterals.begin(); it != stringLiterals.end(); ++it) {
        printf("%s%s", it->c_str(), std::next(it) == stringLiterals.end() ? "" : ", ");
    }
    printf("\n");

    return 0;
}
