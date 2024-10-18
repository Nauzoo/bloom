#ifndef TOKEN_H
#define TOKEN_H

enum tokenTypes{
    TOKEN_KEY_WORD,
    TOKEN_COMMA,
    TOKEN_COLLON,
    TOKEN_SEMI_COLLON,
    TOKEN_LPAR,
    TOKEN_RPAR,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_LCURBRACE,
    TOKEN_RCURBRACE
};

typedef struct {
    char* tk_value;
    enum tokenTypes tk_type;
} Token;

// implement a look up table, such as:
typedef struct { char* key; int value; } symbols;

const char invisibleChars[] = {
    ' ',
    '\n'

};
const char breakChars[] = {
    ';',
    ',',
};

const char blockChars[] = {
    '(',
    ')',
    '[',
    ']',
    '{',
    '}'
};

const char operators[] = {
    '+',
    '-',
    '*',
    '/',
    '=',
    '.',
    '>',
    '<',
    ':',
    '!',
    '#'
};

// har coded shit
const char keyWords[][6] = {
    "if",
    "else",
    "int",
    "float",
    "set"

};
#endif
