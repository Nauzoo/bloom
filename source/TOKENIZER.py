from NODE import *
from ERROR import *


# ---- LEXER ----
class TOKENIZER:
    @staticmethod
    def lexate(code_lines):
        lexed_code = []
        buffer = ''
        op_buffer = ''
        open_string = None
        op_comment = False

        code_lines += '\n'
        for char in code_lines:
            if not op_comment:
                if open_string is None:
                    if char == '#':
                        op_comment = True
                        continue

                    if char not in operators:
                        if len(op_buffer) > 0:
                            lexed_code.append(op_buffer)
                            op_buffer = ''

                    if char == '"' or char == "'":
                        buffer += char
                        open_string = char
                        continue

                    if char == ' ':
                        if len(buffer) > 0:
                            lexed_code.append(buffer)
                            buffer = ''

                    elif char in specialChars:
                        if len(buffer) > 0:
                            lexed_code.append(buffer)  # name=='john'
                            buffer = ''
                        if char in operators:
                            op_buffer += char
                        else:
                            lexed_code.append(char)

                    else:
                        buffer += char

                else:
                    buffer += char
                    if char == open_string:
                        lexed_code.append(buffer)
                        open_string = None
                        buffer = ''
            else:
                if char == '#':
                    op_comment = False

        if len(buffer) > 0:
            ERROR.throw_error(f'(TokenError) Unclosed string {buffer}.')

        return lexed_code

    # ---- TOKENIZER ----

    @staticmethod
    def set_tokens(lexed_text):
        p_nodes = []
        open_num = ''
        float_p = 0
        for i in range(len(lexed_text)):
            each = lexed_text[i]
            if not (each.isnumeric() or each == '.') and len(open_num) > 0:
                if float_p == 0:
                    p_nodes.append(NUM(T_INT, open_num))
                elif float_p == 1:
                    if len(open_num) == 2:
                        open_num += '0'
                    p_nodes.append(NUM(T_FLOAT, open_num))
                else:
                    ERROR.throw_error(f'(SyntaxError) Multiple floating points in number {open_num}.')
                float_p = 0
                open_num = ''

            if each in specialChars:
                if len(open_num) > 0 and each == '.':
                    open_num += each
                    float_p += 1
                else:
                    if each in symbols:
                        p_nodes.append(SYM(each))
                    elif each in operators:
                        p_nodes.append(OPER(each))

            elif each.isnumeric():
                open_num += each

            elif each[0] == "'" or each[0] == '"':
                p_nodes.append(STR(each[1:-1]))

            elif each == 'true' or each == 'false':
                p_nodes.append(BL(each))

            elif each == 'null':
                p_nodes.append(NL())

            else:
                if each.isalnum():
                    p_nodes.append(K(each))
                else:
                    ERROR.throw_error(f'(SyntaxError) The operator "{each}" does not exist.')

        return p_nodes
