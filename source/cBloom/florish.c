#include <stdlib.h>
#include <stdio.h>
#include <threads.h>
#include "lexer.h"

int main(int argc, char *argv[])
{
    FILE * file;
    if (argc > 1) {

        // test if  the file exists [...]

        file = fopen(argv[1], "r");

        // Checking the size of the fille in bytes
        fseek(file, 0L, SEEK_END);
        int fileSize = ftell(file);
        fseek(file, 0L, SEEK_SET);

        char *content = (char*) calloc(fileSize, sizeof(char));
        //char content[fileSize];

        // copying all the content of the file to a single string
        int i = 0;
        int c;
        while((c = fgetc(file)) != EOF){
            content[i] = c;
            i++;
        }

        tokenize(content); // pass file size ?
    }

    //formalize the error messages with it's own struct
    else
        printf("u need to provide a file path.\n");

    return 0;
}
