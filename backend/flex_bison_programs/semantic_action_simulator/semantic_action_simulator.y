%{
#include <stdio.h>
#include <stdlib.h> // For atof, atoi, malloc, free
#include <string.h> // For strdup
#include <math.h>   // For fmod

extern int yylex();
extern int yyerror(const char *s);
extern int yylineno; // Line number from Flex
extern YYSTYPE yylval; // Lexer populates this, so it must be extern here

// Structure to hold variable information in the symbol table
typedef struct {
    char *name;
    enum { INT_TYPE, FLOAT_TYPE, CHAR_TYPE, UNKNOWN_TYPE } type;
    union {
        int ival;
        float fval;
        char cval;
    } value;
} Symbol;

#define MAX_SYMBOLS 100
Symbol symbol_table[MAX_SYMBOLS];
int symbol_count = 0;

Symbol* find_symbol(const char *name) {
    for (int i = 0; i < symbol_count; i++) {
        if (strcmp(symbol_table[i].name, name) == 0) {
            return &symbol_table[i];
        }
    }
    return NULL;
}

Symbol* add_symbol(const char *name, int type) {
    Symbol *sym = find_symbol(name);
    if (sym) {
        // Update type for existing symbol, assume redeclaration in same scope is update for simulation
        sym->type = type;
        return sym;
    }
    if (symbol_count < MAX_SYMBOLS) {
        sym = &symbol_table[symbol_count++];
        sym->name = strdup(name);
        sym->type = type;
        return sym;
    }
    fprintf(stderr, "Error: Symbol table full. Cannot add '%s' at line %d\n", name, yylineno);
    return NULL;
}

void yyerror(const char *s) {
    fprintf(stderr, "PARSER ERROR: %s at line %d\n", s, yylineno);
}

%}

%define parse.error verbose

%union {
    int ival;
    float fval;
    char cval;
    char *str_val; // For identifiers, types, string literals
}

// Tokens from Lexer
%token <str_val> IDENTIFIER TYPE_INT TYPE_FLOAT TYPE_CHAR TYPE_VOID TYPE_DOUBLE TYPE_LONG TYPE_SHORT
%token <ival> INT_LITERAL
%token <fval> FLOAT_LITERAL
%token <cval> CHAR_LITERAL
%token <str_val> STRING_LITERAL // For handling #include, printf

%token CONST_QUALIFIER SIGNED_QUALIFIER UNSIGNED_QUALIFIER // Type Qualifiers
%token ADD SUB MUL DIV MOD ASTERISK // Arithmetic and pointer
%token ASSIGN EQ_OP NE_OP LT_OP GT_OP LE_OP GE_OP AND_OP OR_OP NOT_OP AMPERSAND // Operators

%token LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET SEMICOLON COMMA EOL // Punctuation

// Keywords to ignore (or parse and then ignore)
%token IF_KEYWORD ELSE_KEYWORD WHILE_KEYWORD FOR_KEYWORD RETURN_KEYWORD MAIN_KEYWORD PRINTF_KEYWORD INCLUDE_KEYWORD
%token SWITCH_KEYWORD DO_KEYWORD GOTO_KEYWORD CONTINUE_KEYWORD BREAK_KEYWORD

// Operator precedence (similar to C)
%left OR_OP
%left AND_OP
%left EQ_OP NE_OP
%left LT_OP GT_OP LE_OP GE_OP
%left ADD SUB
%left MUL DIV MOD
%right NOT_OP ASTERISK AMPERSAND // Unary operators and address-of

%type <ival> int_expression_result
%type <fval> float_expression_result
%type <cval> char_expression_result
%type <str_val> type_specifier declaration_specifiers
%type <str_val> declarator direct_declarator identifier_list
%type <str_val> constant_expression

%start program

%%

program:
    preprocessor_directives function_definitions
    ;

preprocessor_directives:
    /* empty */
    | preprocessor_directives preprocessor_directive
    ;

preprocessor_directive:
    INCLUDE_KEYWORD STRING_LITERAL EOL { if($2) free($2); } // Basic #include handling
    | INCLUDE_KEYWORD IDENTIFIER EOL { if($2) free($2); } // For <stdio.h> type includes (IDENTIFIER token)
    | error EOL { yyclearin; yyerrok; } // Error recovery for preprocessor lines
    ;

function_definitions:
    /* empty */
    | function_definitions function_definition
    ;

function_definition:
    TYPE_INT MAIN_KEYWORD LPAREN RPAREN compound_statement {
        // Here we could free associated strings if TYPE_INT or MAIN_KEYWORD were str_val
        // but they are direct tokens.
    }
    | TYPE_VOID MAIN_KEYWORD LPAREN RPAREN compound_statement {
        // Handle void main() as well
    }
    ;

compound_statement:
    LBRACE statement_list RBRACE
    ;

statement_list:
    /* empty */
    | statement_list statement EOL { /* Process statement followed by EOL */ }
    | statement_list EOL { /* Handle empty lines within compound statements */ }
    ;

statement:
    declaration SEMICOLON
    | assignment SEMICOLON
    | RETURN_KEYWORD int_expression_result SEMICOLON { /* Ignore return statement */ }
    | RETURN_KEYWORD SEMICOLON { /* Ignore return statement */ }
    | error SEMICOLON { yyclearin; yyerrok; } // Basic error recovery for a statement
    | error { yyclearin; yyerrok; } // Basic error recovery for a statement without semicolon
    ;

declaration:
    declaration_specifiers init_declarator_list {
        if ($1) free($1); // Free the combined type string
    }
    ;

declaration_specifiers:
    type_specifier {
        $$ = $1;
    }
    | type_qualifier declaration_specifiers {
        char *temp = (char *)malloc(strlen($1) + 1 + strlen($2) + 1);
        sprintf(temp, "%s %s", $1, $2);
        $$ = strdup(temp);
        free($1); free($2); free(temp);
    }
    | declaration_specifiers type_qualifier {
        char *temp = (char *)malloc(strlen($1) + 1 + strlen($2) + 1);
        sprintf(temp, "%s %s", $1, $2);
        $$ = strdup(temp);
        free($1); free($2); free(temp);
    }
    ;

type_qualifier:
    CONST_QUALIFIER     { $$ = strdup("const"); }
    | SIGNED_QUALIFIER  { $$ = strdup("signed"); }
    | UNSIGNED_QUALIFIER { $$ = strdup("unsigned"); }
    | TYPE_LONG         { $$ = strdup("long"); }
    | TYPE_SHORT        { $$ = strdup("short"); }
    ;

type_specifier:
    TYPE_VOID           { $$ = strdup("void"); }
    | TYPE_CHAR         { $$ = strdup("char"); }
    | TYPE_SHORT        { $$ = strdup("short"); }
    | TYPE_INT          { $$ = strdup("int"); }
    | TYPE_LONG         { $$ = strdup("long"); }
    | TYPE_FLOAT        { $$ = strdup("float"); }
    | TYPE_DOUBLE       { $$ = strdup("double"); }
    ;

init_declarator_list:
    init_declarator
    | init_declarator_list COMMA init_declarator
    ;

init_declarator:
    declarator {
        // If it's just a declaration, add to symbol table, but don't print yet (no assignment)
        Symbol *sym = add_symbol($1, UNKNOWN_TYPE); // Type will be determined by declaration_specifiers later
        if (sym && current_type_specifier) { // Use the type passed down from declaration_specifiers, stored in current_type_specifier
            if (strcmp(current_type_specifier, "int") == 0) sym->type = INT_TYPE;
            else if (strcmp(current_type_specifier, "float") == 0) sym->type = FLOAT_TYPE;
            else if (strcmp(current_type_specifier, "char") == 0) sym->type = CHAR_TYPE;
            // No printing for bare declarations
        }
        if ($1) free($1);
    }
    | declarator ASSIGN constant_expression {
        // This is an assignment in declaration, handle and print it
        Symbol *sym = find_symbol($1);
        if (!sym) { // If not found, add it (first declaration with assignment)
            int type_enum = UNKNOWN_TYPE;
            if (current_type_specifier) {
                if (strcmp(current_type_specifier, "int") == 0) type_enum = INT_TYPE;
                else if (strcmp(current_type_specifier, "float") == 0) type_enum = FLOAT_TYPE;
                else if (strcmp(current_type_specifier, "char") == 0) type_enum = CHAR_TYPE;
            }
            sym = add_symbol($1, type_enum);
        }

        if (sym) {
            // Determine the type of the constant expression and assign
            // This is a simplification; a full C compiler would parse the actual type
            // Here, we convert $3 (string) to appropriate type based on variable type
            if (sym->type == INT_TYPE) {
                sym->value.ival = atoi($3);
                printf("- %s = %d\n", sym->name, sym->value.ival);
            } else if (sym->type == FLOAT_TYPE) {
                sym->value.fval = atof($3);
                printf("- %s = %.2f\n", sym->name, sym->value.fval);
            } else if (sym->type == CHAR_TYPE) {
                sym->value.cval = $3[0]; // Take first char if it's a string constant
                printf("- %s = '%c'\n", sym->name, sym->value.cval);
            } else {
                fprintf(stderr, "Error: Variable '%s' has an unknown type for assignment in declaration at line %d\n", sym->name, yylineno);
            }
        }
        if ($1) free($1);
        if ($3) free($3);
    }
    ;

declarator:
    ASTERISK declarator {
        // Pointers. Strip '*' from name. Just pass the identifier part up.
        // We only care about the base identifier. 
        // The type needs to reflect it's a pointer if we were doing full type checking.
        // For this simulator, we just pass the variable name.
        $$ = $2; // Pass the identifier string up
    }
    | IDENTIFIER {
        $$ = $1; // Pass the identifier string up
    }
    ;

assignment:
    IDENTIFIER ASSIGN int_expression_result SEMICOLON { // For int/char assignments
        Symbol *sym = find_symbol($1);
        if (sym) {
            if (sym->type == INT_TYPE) {
                sym->value.ival = $3;
                printf("- %s = %d\n", sym->name, sym->value.ival);
            } else if (sym->type == FLOAT_TYPE) { // Implicit int to float conversion
                sym->value.fval = (float)$3;
                printf("- %s = %.2f\n", sym->name, sym->value.fval);
            } else if (sym->type == CHAR_TYPE) { // Implicit int to char conversion
                sym->value.cval = (char)$3;
                printf("- %s = '%c'\n", sym->name, sym->value.cval);
            } else {
                fprintf(stderr, "Error: Variable '%s' has an unknown type for assignment at line %d\n", sym->name, yylineno);
            }
        } else {
            fprintf(stderr, "Error: Undeclared variable '%s' at line %d\n", $1, yylineno);
        }
        free($1);
    }
    | IDENTIFIER ASSIGN float_expression_result SEMICOLON { // For float assignments
        Symbol *sym = find_symbol($1);
        if (sym) {
            if (sym->type == INT_TYPE) { // Implicit float to int conversion
                sym->value.ival = (int)$3;
                printf("- %s = %d\n", sym->name, sym->value.ival);
            } else if (sym->type == FLOAT_TYPE) {
                sym->value.fval = $3;
                printf("- %s = %.2f\n", sym->name, sym->value.fval);
            } else if (sym->type == CHAR_TYPE) { // Implicit float to char conversion
                sym->value.cval = (char)$3;
                printf("- %s = '%c'\n", sym->name, sym->value.cval);
            } else {
                fprintf(stderr, "Error: Variable '%s' has an unknown type for assignment at line %d\n", sym->name, yylineno);
            }
        } else {
            fprintf(stderr, "Error: Undeclared variable '%s' at line %d\n", $1, yylineno);
        }
        free($1);
    }
    | IDENTIFIER ASSIGN char_expression_result SEMICOLON { // For char assignments
        Symbol *sym = find_symbol($1);
        if (sym) {
            if (sym->type == INT_TYPE) { // Implicit char to int conversion
                sym->value.ival = (int)$3;
                printf("- %s = %d\n", sym->name, sym->value.ival);
            } else if (sym->type == FLOAT_TYPE) { // Implicit char to float conversion
                sym->value.fval = (float)$3;
                printf("- %s = %.2f\n", sym->name, sym->value.fval);
            } else if (sym->type == CHAR_TYPE) {
                sym->value.cval = $3;
                printf("- %s = '%c'\n", sym->name, sym->value.cval);
            } else {
                fprintf(stderr, "Error: Variable '%s' has an unknown type for assignment at line %d\n", sym->name, yylineno);
            }
        } else {
            fprintf(stderr, "Error: Undeclared variable '%s' at line %d\n", $1, yylineno);
        }
        free($1);
    }
    ;

expression_statement:
    // For now, any expression followed by a semicolon is an expression statement.
    // We will ignore its value.
    expression_result
    | int_expression_result
    | float_expression_result
    | char_expression_result
    ;

expression_result: // A generic expression result (needed for expression_statement to consume)
    int_expression_result       { }
    | float_expression_result   { }
    | char_expression_result    { }
    ;

// Generic C statements that we parse and ignore for simulation purposes
labeled_statement:
    IDENTIFIER ':' statement // for goto labels
    ;

selection_statement:
    IF_KEYWORD LPAREN expression_result RPAREN statement
    | IF_KEYWORD LPAREN expression_result RPAREN statement ELSE_KEYWORD statement
    | SWITCH_KEYWORD LPAREN expression_result RPAREN compound_statement // Assuming SWITCH_KEYWORD token exists
    ;

iteration_statement:
    WHILE_KEYWORD LPAREN expression_result RPAREN statement
    | DO_KEYWORD statement WHILE_KEYWORD LPAREN expression_result RPAREN SEMICOLON // Assuming DO_KEYWORD token exists
    | FOR_KEYWORD LPAREN expression_result SEMICOLON expression_result SEMICOLON expression_result RPAREN statement
    ;

jump_statement:
    GOTO_KEYWORD IDENTIFIER SEMICOLON // Assuming GOTO_KEYWORD token exists
    | CONTINUE_KEYWORD SEMICOLON // Assuming CONTINUE_KEYWORD token exists
    | BREAK_KEYWORD SEMICOLON // Assuming BREAK_KEYWORD token exists
    | RETURN_KEYWORD expression_result SEMICOLON
    | RETURN_KEYWORD SEMICOLON
    ;

// --- Constant expression for initializer
constant_expression:
    INT_LITERAL             { $$ = (char*)malloc(sizeof(char) * 20); sprintf($$, "%d", $1); }
    | FLOAT_LITERAL           { $$ = (char*)malloc(sizeof(char) * 20); sprintf($$, "%.2f", $1); }
    | CHAR_LITERAL            { $$ = (char*)malloc(sizeof(char) * 2); sprintf($$, "%c", $1); }
    | STRING_LITERAL        { $$ = strdup($1); }
    | IDENTIFIER            { $$ = strdup($1); } // If a const identifier is used as an initializer

// --- Expression Evaluation ---
// These rules handle type promotion and evaluation.
// Operator precedence is defined by %left/%right directives.

int_expression_result:
    INT_LITERAL             { $$ = $1; }
    | CHAR_LITERAL          { $$ = (int)$1; }
    | LPAREN int_expression_result RPAREN { $$ = $2; }
    | IDENTIFIER            {
        Symbol *sym = find_symbol($1);
        if (sym) {
            if (sym->type == INT_TYPE) { $$ = sym->value.ival; }
            else if (sym->type == FLOAT_TYPE) { $$ = (int)sym->value.fval; } // Implicit conversion
            else if (sym->type == CHAR_TYPE) { $$ = (int)sym->value.cval; } // Implicit conversion
            else { fprintf(stderr, "Error: Variable '%s' has unknown type at line %d\n", $1, yylineno); YYABORT; }
        } else { fprintf(stderr, "Error: Undeclared variable '%s' at line %d\n", $1, yylineno); YYABORT; }
        free($1);
    }
    | int_expression_result ADD int_expression_result { $$ = $1 + $3; }
    | int_expression_result SUB int_expression_result { $$ = $1 - $3; }
    | int_expression_result MUL int_expression_result { $$ = $1 * $3; }
    | int_expression_result DIV int_expression_result {
        if ($3 == 0) { fprintf(stderr, "Error: Integer division by zero at line %d\n", yylineno); YYABORT; }
        $$ = $1 / $3;
    }
    | int_expression_result MOD int_expression_result {
        if ($3 == 0) { fprintf(stderr, "Error: Integer modulo by zero at line %d\n", yylineno); YYABORT; }
        $$ = $1 % $3;
    }
    | float_expression_result { $$ = (int)$1; } // Convert float result to int
    ;

float_expression_result:
    FLOAT_LITERAL           { $$ = $1; }
    | INT_LITERAL           { $$ = (float)$1; } // Promote int to float
    | CHAR_LITERAL          { $$ = (float)$1; }
    | LPAREN float_expression_result RPAREN { $$ = $2; }
    | IDENTIFIER            {
        Symbol *sym = find_symbol($1);
        if (sym) {
            if (sym->type == INT_TYPE) { $$ = (float)sym->value.ival; }
            else if (sym->type == FLOAT_TYPE) { $$ = sym->value.fval; }
            else if (sym->type == CHAR_TYPE) { $$ = (float)sym->value.cval; }
            else { fprintf(stderr, "Error: Variable '%s' has unknown type at line %d\n", $1, yylineno); YYABORT; }
        } else { fprintf(stderr, "Error: Undeclared variable '%s' at line %d\n", $1, yylineno); YYABORT; }
        free($1);
    }
    | float_expression_result ADD float_expression_result { $$ = $1 + $3; }
    | float_expression_result SUB float_expression_result { $$ = $1 - $3; }
    | float_expression_result MUL float_expression_result { $$ = $1 * $3; }
    | float_expression_result DIV float_expression_result {
        if ($3 == 0.0f) { fprintf(stderr, "Error: Float division by zero at line %d\n", yylineno); YYABORT; }
        $$ = $1 / $3;
    }
    | int_expression_result { $$ = (float)$1; } // Convert int result to float
    ;

char_expression_result:
    CHAR_LITERAL            { $$ = $1; }
    | INT_LITERAL           { $$ = (char)$1; } // Convert int to char
    | LPAREN char_expression_result RPAREN { $$ = $2; }
    | IDENTIFIER            {
        Symbol *sym = find_symbol($1);
        if (sym) {
            if (sym->type == CHAR_TYPE) { $$ = sym->value.cval; }
            else if (sym->type == INT_TYPE) { $$ = (char)sym->value.ival; }
            else if (sym->type == FLOAT_TYPE) { $$ = (char)sym->value.fval; }
            else { fprintf(stderr, "Error: Variable '%s' has unknown type at line %d\n", $1, yylineno); YYABORT; }
        } else { fprintf(stderr, "Error: Undeclared variable '%s' at line %d\n", $1, yylineno); YYABORT; }
        free($1);
    }
    | char_expression_result ADD char_expression_result { $$ = $1 + $3; } // Char arithmetic is int arithmetic
    | char_expression_result SUB char_expression_result { $$ = $1 - $3; }
    | char_expression_result MUL char_expression_result { $$ = $1 * $3; }
    | char_expression_result DIV char_expression_result {
        if ($3 == 0) { fprintf(stderr, "Error: Char division by zero (int conversion) at line %d\n", yylineno); YYABORT; }
        $$ = $1 / $3;
    }
    | int_expression_result { $$ = (char)$1; } // Convert int result to char
    ;

%%

int main() {
    // This main is usually not used when integrated with Python.
    // Python will call yylex/yyparse directly.
    return 0;
}
