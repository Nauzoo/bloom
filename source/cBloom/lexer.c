#include "lexer.h"
#include "token.h"
#include <string.h>
#include <stddef.h>
#include <stdio.h>
#include <strings.h>
#include <stdbool.h>
#include <wchar.h>


bool isInvisibleChar(char character){
    // checking for invisible chars ' ' and '\n'
    for (int i = 0; i < sizeof(invisibleChars); i++){
        if (character == invisibleChars[i])
            return true;
    }
    return false;
}

bool isBreakChar(char character){
    // verifying if character is a breakable
    for (int i = 0; i < sizeof(breakChars); i++){
        if (character == breakChars[i])
            return true;
    }
    return false;
}

bool isBlockChar(char character){
    for (int i = 0; i < sizeof(blockChars); i++){
        if (character == blockChars[i])
            return true;
    }
    return false;
}

bool isOperator(char character){
    for (int i = 0; i < sizeof(operators); i++){
        if (character == operators[i])
            return true;
    }
    return false;
}

bool isSpecialChar(char character) {
    if (isInvisibleChar(character) ||
            isBreakChar(character) ||
            isBlockChar(character) ||
            isOperator(character)
        )
        return true;
    else
        return false;
}


Token getToken(char term[]) {
    Token tk = {term, TOKEN_KEY_WORD};
    printf("%s\n", tk.tk_value);
    return tk;
}

Token* tokenize(char text[]) {

    int textSize = strlen(text);

    char term[20]; // TODO: check wether a term has to be limited
    int termIndex = 0;
    char currenChar;

    for (int i = 0; i < textSize; i++){
        currenChar = text[i];
        if (!isSpecialChar(currenChar)){
            term[termIndex] = currenChar;
            termIndex++;
        }
        else {
            if (strlen(term) > 0)
                getToken(term);
            if (!isInvisibleChar(currenChar))
                getToken(&currenChar);
            termIndex = 0;
            memset(term, 0, 20); // hard coded shit
        }

    }

    return NULL;
}

