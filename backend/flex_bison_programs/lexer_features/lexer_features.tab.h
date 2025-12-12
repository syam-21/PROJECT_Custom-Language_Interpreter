
/* A Bison parser, made by GNU Bison 2.4.1.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     IF_KW = 258,
     ELSE_KW = 259,
     WHILE_KW = 260,
     FOR_KW = 261,
     RETURN_KW = 262,
     TYPE_INT = 263,
     TYPE_FLOAT = 264,
     TYPE_STRING = 265,
     IDENTIFIER = 266,
     NUMBER = 267,
     STRING_LITERAL = 268,
     OP_PLUS = 269,
     OP_MINUS = 270,
     OP_MUL = 271,
     OP_DIV = 272,
     OP_ASSIGN = 273,
     OP_EQ = 274,
     OP_NE = 275,
     OP_LT = 276,
     OP_GT = 277,
     OP_LE = 278,
     OP_GE = 279,
     OP_AND = 280,
     OP_OR = 281,
     OP_NOT = 282,
     DEL_LP = 283,
     DEL_RP = 284,
     DEL_LC = 285,
     DEL_RC = 286,
     DEL_LB = 287,
     DEL_RB = 288,
     DEL_SEMICOLON = 289,
     DEL_COMMA = 290,
     DEL_DOT = 291
   };
#endif



#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 1676 of yacc.c  */
#line 22 "C:\\Users\\siyam\\OneDrive\\Desktop\\project_cod\\backend\\flex_bison_programs\\lexer_features\\lexer_features.y"

    char *str_val;
    float float_val; // Kept for compatibility with the lexer, though not used for output



/* Line 1676 of yacc.c  */
#line 95 "lexer_features.tab.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


