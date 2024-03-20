from sys import *
from RUNTIME import *
from ERROR import *


def initialize(file):
    if file.endswith('.bloom'):
        code = open(file, 'r').read()
        return code
    else:
        ERROR.throw_error('(AccessError) File extension does not match with ".bloom". You have to open a bloom file!')


def run_time(ast):
    code_tree = ast.tree

    for index in range(len(code_tree)):
        pass


if __name__ == '__main__':
    # parser = PARSER.PARSER()
    # tokenizer = TOKENIZER.TOKENIZER()
    run_time = RUNTIME()

    '''print(parser.parse(
        lexer.set_tokens(
            lexer.lexate(
                initialize(argv[1])))).self_write())'''

    '''for e in lexer.set_tokens(
        lexer.lexate(
            initialize(argv[1]))):
        print(e.self_write())'''

    run_time.exec(
        parser.parse(
                lexer.set_tokens(
                    lexer.lexate(
                        initialize(argv[1])))))

    # run_time(parser(lexer(initialize(argv[1]))))
    # print(SOLID_DATA)
