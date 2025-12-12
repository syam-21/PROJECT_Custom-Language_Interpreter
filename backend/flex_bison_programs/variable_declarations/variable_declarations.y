%{
#include <stdio.h>
#include <stdlib.h> // For free
#include <string.h> // For strdup

extern int yylex();
extern int yyerror(const char *s);
extern FILE *yyin;
extern int yylineno; // Line number from Flex



char *current_type_specifier = NULL; // To hold the type across multiple declarators

%}

%define parse.error verbose

%token <str_val> IDENTIFIER TYPE_SPECIFIER
%token SEMICOLON COMMA ASSIGN NUMBER ASTERISK

// Reserved C keywords that are not directly types or part of variable names
%token AUTO BREAK CASE CONST CONTINUE DEFAULT DO ELSE ENUM EXTERN FOR GOTO IF INLINE REGISTER RESTRICT RETURN SIZEOF STATIC STRUCT SWITCH TYPEDEF UNION VOLATILE WHILE
%token TYPE_CHAR TYPE_DOUBLE TYPE_FLOAT TYPE_INT TYPE_LONG TYPE_SHORT TYPE_VOID SIGNED UNSIGNED

%type <str_val> type_qualifier type_specifier declaration_specifiers
%type <str_val> declarator direct_declarator

%start program

%%

program:
    /* empty */
    | program declaration_statement
    ;

declaration_statement:
    declaration_specifiers declarator_list SEMICOLON {
        // current_type_specifier will be set by declaration_specifiers
        // Actions for declarator_list handle printing
        if (current_type_specifier) {
            free(current_type_specifier);
            current_type_specifier = NULL;
        }
    }
    | error SEMICOLON { yyclearin; yyerrok; fprintf(stderr, "Error: Invalid declaration statement skipped at line %d.\n", yylineno); }
    | error { yyclearin; yyerrok; fprintf(stderr, "Error: Invalid input, recovering at line %d.\n", yylineno); }
    ;

declaration_specifiers:
    TYPE_SPECIFIER {
        if (current_type_specifier) free(current_type_specifier);
        current_type_specifier = strdup($1);
        $$ = strdup($1); // Pass the type string
    }
    | type_qualifier declaration_specifiers {
        // Concatenate type_qualifier (e.g., "unsigned") with type_specifier (e.g., "int")
        char *temp = (char *)malloc(strlen($1) + 1 + strlen($2) + 1);
        sprintf(temp, "%s %s", $1, $2);
        if (current_type_specifier) free(current_type_specifier);
        current_type_specifier = strdup(temp);
        $$ = strdup(temp);
        free($1); free($2); free(temp);
    }
    | declaration_specifiers type_qualifier {
        // Handle cases like "int unsigned" -> "unsigned int"
        char *temp = (char *)malloc(strlen($1) + 1 + strlen($2) + 1);
        sprintf(temp, "%s %s", $1, $2);
        if (current_type_specifier) free(current_type_specifier);
        current_type_specifier = strdup(temp);
        $$ = strdup(temp);
        free($1); free($2); free(temp);
    }
    ;

type_qualifier:
    SIGNED      { $$ = strdup("signed"); }
    | UNSIGNED  { $$ = strdup("unsigned"); }
    | CONST     { $$ = strdup("const"); }
    | VOLATILE  { $$ = strdup("volatile"); }
    | AUTO      { $$ = strdup("auto"); } // Usually a storage class specifier
    | REGISTER  { $$ = strdup("register"); }
    | STATIC    { $$ = strdup("static"); }
    | EXTERN    { $$ = strdup("extern"); }
    | RESTRICT  { $$ = strdup("restrict"); }
    | INLINE    { $$ = strdup("inline"); }
    | LONG      { $$ = strdup("long"); } // Correctly placed
    | SHORT     { $$ = strdup("short"); } // Correctly placed
    ;

declarator_list:
    declarator {
        // Printing is handled by declarator action
    }
    | declarator_list COMMA declarator {
        // Printing is handled by declarator action
    }
    ;

declarator:
    ASTERISK declarator {
        $$ = $2; // Pass the identifier part up from the inner declarator
    }
    | direct_declarator { $$ = $1; } // Pass the identifier part up
    ;

direct_declarator:
    IDENTIFIER {
        if (current_type_specifier) {
            printf("- Declare %s %s\n", current_type_specifier, $1);
        } else {
            printf("- Declare UnknownType %s\n", $1);
        }
        $$ = $1; // Pass the identifier string up
    }
    | IDENTIFIER ASSIGN /* IGNORE VALUE */ {
        if (current_type_specifier) {
            printf("- Declare %s %s\n", current_type_specifier, $1);
        } else {
            printf("- Declare UnknownType %s\n", $1);
        }
        $$ = $1; // Pass the identifier string up
        // We explicitly ignore everything after ASSIGN until the next COMMA or SEMICOLON
        // The lexer handles skipping numbers, and parser rules would skip other parts.
        // For simplicity here, we assume lexer skipped values.
        // To be more robust, a rule like 'assignment_expression' would go here
        // and its content would be discarded. For now, the ASSIGN token itself is sufficient
        // for the grammar to recognize an initialization, and the lexer ignores the value tokens.
    }
    ;

%%

int yyerror(const char *s) {
    fprintf(stderr, "Error: %s at line %d\n", s, yylineno);
    return 0;
}

int main() {
    // This main is for testing purposes if compiled directly.
    // In our setup, yylex and yyparse will be called by the Python wrapper.
    // For now, an empty main or omitted main is fine as long as yylex/yyparse are accessible.
    // The Python utility will manage the input stream (yyin) and call yyparse.
    return 0;
}
