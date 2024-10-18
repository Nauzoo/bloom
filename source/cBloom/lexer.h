#ifndef LEXER_H
#define LEXER_H

#include "token.h"

Token* tokenize(char text[]);
Token getToken(char term[]);

#endif
