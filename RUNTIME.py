import TOKENIZER
import PARSER
from NODE import NL, NUM, STR, BL, ARR, FUN
from DEPENDENCIES import *
from ERROR import *

lexer = TOKENIZER.TOKENIZER()
parser = PARSER.PARSER()


class RUNTIME:
    def exec(self, ast):
        last_condition_state = None
        for c in ast.tree:

            if c.my_type != N_COND_STATEMENT and last_condition_state is not None:
                last_condition_state = None
            elif c.my_type == N_COND_STATEMENT:
                if c.layer == 'if' and last_condition_state is not None:
                    last_condition_state = None

            if c.my_type == N_DECLARATION:
                if c.get_key() is None:
                    ERROR.throw_error('(SyntaxError) Tried create unnamed variable.')
                if c.get_reserve() == 'multiple':
                    SOLID_DATA[c.get_key()] = ARR()
                else:
                    SOLID_DATA[c.get_key()] = NL()

            elif c.my_type == N_DELETATION:
                key = c.get_value()

                if key.my_type == N_KEY:
                    k = key.syn_obj
                    if SOLID_DATA.get(k) is not None:
                        SOLID_DATA.pop(k)
                    else:
                        ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {k}, declare this '
                                          f'variable first!')

                elif key.my_type == N_ARR_ACCESS:
                    k = key.get_key()
                    indexes = key.get_indexes()
                    address_pointer = SOLID_DATA[k]
                    mod = None
                    for i in range(len(indexes)):
                        if i == len(indexes) - 1:
                            mod = 'del'
                        address_pointer = self.scarve_array(address_pointer, indexes[i], mod)
                else:
                    ERROR.throw_error('(TypeError) "del" only take a memory address as parameter. ')

            elif c.my_type == N_ASSIGNMENT:
                key = c.get_key()          # returns expread / arraccess
                value = c.get_value()

                ac_key = key.get_key()
                memory_address = SOLID_DATA.get(ac_key)
                if memory_address is not None:
                    resolved_v = self.solve_exp(value)

                    if key.my_type == N_EXP_READ:
                        if SOLID_DATA[ac_key].my_type == N_ARRAY:
                            if resolved_v.my_type == N_ARRAY:
                                SOLID_DATA[ac_key] = resolved_v
                            else:
                                ERROR.throw_error(f'(AssignmentError) Tried to assign single value "{ac_key}" '
                                                  f'to array memory address.')

                        elif SOLID_DATA[ac_key].my_type == N_FUN:
                            if resolved_v.my_type == N_FUN:
                                SOLID_DATA[ac_key] = resolved_v
                            else:
                                ERROR.throw_error(f'(AssignmentError) Tried to assign {resolved_v.my_type} "{ac_key}" '
                                                  f'to function memory address.')
                        else:
                            if resolved_v.my_type in N_NUM + N_STR + N_BOOL + N_NULL:
                                SOLID_DATA[ac_key] = resolved_v
                            else:
                                ERROR.throw_error(f'(AssignmentError) Tried to assign array "{ac_key}" '
                                                  f'to single value memory address.')

                    elif key.my_type == N_ARR_ACCESS:
                        indexes = key.get_indexes()
                        address_pointer = SOLID_DATA[ac_key]
                        mod = None
                        for i in range(len(indexes)):
                            if i == len(indexes)-1:
                                mod = 'add'
                            address_pointer = self.scarve_array(address_pointer, indexes[i], mod, resolved_v)

                else:
                    ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {ac_key}, declare this '
                                      f'variable first!')

            elif c.my_type == N_C_WRITE:
                value = c.get_value()
                res = self.solve_exp(value)
                res.write_to_console()
                print()

            elif c.my_type == N_COND_STATEMENT:
                if last_condition_state is None:
                    if c.layer == 'if':
                        value = c.get_value()
                        last_condition_state = False
                        if self.solve_exp(value).syn_obj == 'true':
                            self.exec(parser.parse(c.get_exeblock().get_block()))  # rever a necessidade de um node codeblock
                            last_condition_state = True
                    else:
                        ERROR.throw_error(f'(SyntaxError) Expected if statement before "{c.layer}".')

                elif last_condition_state is False:
                    if c.layer == 'elsif':
                        value = c.get_value()
                        if self.solve_exp(value).syn_obj == 'true':
                            self.exec(parser.parse(c.get_exeblock().get_block()))
                            last_condition_state = True
                    else:
                        self.exec(parser.parse(c.get_exeblock().get_block()))
                        last_condition_state = True

            elif c.my_type == N_WHILE_LOOP:
                value = c.get_value()
                if c.get_exeblock() is None:
                    ERROR.throw_error('(SyntaxError) While loop requires a block ({...}).')
                while self.solve_exp(value).syn_obj == 'true':
                    self.exec(parser.parse(c.get_exeblock().get_block()))

            elif c.my_type == N_FOR_LOOP:
                from_op = c.get_value()
                block = c.get_exeblock()

                if from_op is not None:
                    dec = from_op.get_v1()
                    arr = from_op.get_v2()

                    key = None
                    if dec.my_type == N_DECLARATION:
                        key = dec.get_key()
                        if dec.get_reserve() == 'multiple':
                            SOLID_DATA[key] = ARR()
                        else:
                            SOLID_DATA[key] = NL()
                    else:
                        ERROR.throw_error(f'(TypeError) For needs a variable declaration as first parameter, you gave '
                                          f'"{dec.my_type}" instead.')

                    if arr.my_type == N_TO_OP:
                        arr = self.solve_exp(arr)

                    elif arr.my_type == N_KEY:
                        if SOLID_DATA.get(arr.syn_obj) is not None:
                            arr = SOLID_DATA[arr.syn_obj]
                        else:
                            ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {arr.syn_obj}, declare this '
                                              f'variable first!')

                    if arr.my_type != N_ARRAY:
                        ERROR.throw_error(f'(TypeError) For needs an array as second parameter, you gave '
                                          f'"{arr.my_type}" instead.')

                    for each in arr.get_node_list():
                        SOLID_DATA[key] = each
                        if block is None:
                            ERROR.throw_error('(SyntaxError) For loop requires a block ({...}).')
                        self.exec(parser.parse(block.get_block()))
                else:
                    ERROR.throw_error('(AssignmentError) the for loop has no declaration attached to it')

            elif c.my_type == N_FUN_DEC:
                key = c.get_key()

                if key is None:
                    ERROR.throw_error('(SyntaxError) Tried to create an unnamed function.')
                if c.get_exeblock() is None:
                    ERROR.throw_error('(SyntaxError) Function requires a block ({...}).')

                parameter_labels = []
                if SOLID_DATA.get(key) is None:
                    if c.get_parameters() is None:
                        ERROR.throw_error('(AssignmentError) Function declaration requires parenthesis.')
                    for parameter in c.get_parameters().get_node_array():
                        if parameter.my_type == 'AST':
                            for n in parameter.tree:
                                if n.my_type == N_DECLARATION:
                                    parameter_labels.append(n.get_key())
                                if n.my_type != N_DECLARATION:
                                    ERROR.throw_error(f'(TypeError) You can only set declarations as '
                                                      f'function creation parameters, you gave {n.my_type} instead.')

                            self.exec(parameter)
                        elif parameter.my_type == N_NULL:
                            parameter_labels.append(parameter.syn_obj)
                        else:
                            ERROR.throw_error(f'(TypeError) You can only set declarations as '
                                              f'function creation parameters, you gave {parameter.my_type} instead.')
                    SOLID_DATA[key] = FUN(parameter_labels, c.get_exeblock())

                else:
                    ERROR.throw_error(f"(AssignmentError) The label {key} is already reserved, change this function's "
                                      f'name.')

            elif c.my_type == N_FUN_CALL:
                key = c.get_key()
                pars = c.get_parameters().get_node_array()

                memory_address = SOLID_DATA.get(key)
                if memory_address is not None:
                    memory_address = SOLID_DATA[key]
                    if memory_address.my_type == N_FUN:
                        mother_pars = memory_address.get_parameters()

                        m_counts = 0
                        p_counts = 0

                        for each in mother_pars:
                            if each != 'null':
                                m_counts += 1

                        for each in pars:
                            if each.my_type != N_NULL:
                                p_counts += 1

                        if p_counts > m_counts:
                            ERROR.throw_error(f'(AccessError) Parameter overload ({p_counts-m_counts}) '
                                              f'in function "{key}"')
                        if p_counts < m_counts:
                            ERROR.throw_error(f'(AccessError) Parameters unfilled ({m_counts-p_counts}) '
                                              f'in function "{key}"')

                        if len(mother_pars) <= len(pars):
                            for i in range(0, len(mother_pars)):
                                SOLID_DATA[mother_pars[i]] = self.solve_icognite(pars[i])
                    else:
                        ERROR.throw_error(f'(CallError) You tried to call "{key}", which is not a function. '
                                          f'Call only functions.')

                    self.exec(parser.parse(memory_address.get_exeblock().get_block()))

                else:
                    ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {key}, declare this '
                                      f'variable first!')

            # print(SOLID_DATA)

    def solve_exp(self, operation):
        res = NL()
        n_res = None
        s_res = ''

        if operation is None:
            ERROR.throw_error('(OperationError) Unsolved expression. Did you forget to close any structure?')

        if operation.my_type == N_BINARYOP:
            i1 = operation.get_v1()
            i2 = operation.get_v2()

            i1 = self.solve_icognite(i1)
            i2 = self.solve_icognite(i2)

            if i1.my_type == i2.my_type:
                if i1.my_type == N_NUM and i2.my_type == N_NUM:
                    i1 = int(i1.syn_obj) if '.' not in i1.syn_obj else float(i1.syn_obj)
                    i2 = int(i2.syn_obj) if '.' not in i2.syn_obj else float(i2.syn_obj)
                    if operation.op == SUM:
                        n_res = i1 + i2
                    elif operation.op == SUB:
                        n_res = i1 - i2
                    elif operation.op == MUL:
                        n_res = i1 * i2
                    elif operation.op == DIV:
                        if i2 != 0:
                            n_res = i1 / i2
                        else:
                            ERROR.throw_error(f'(ZeroDivError) Tried to divide by zero!')
                elif i1.my_type == N_STR and i2.my_type == N_STR:
                    if operation.op == SUM:
                        i1 = i1.syn_obj
                        i2 = i2.syn_obj
                        s_res = i1 + i2
                    else:
                        ERROR.throw_error(f'(OperationError) You can only perform {operation.op} operation '
                                          f'between numbers.')
            else:
                ERROR.throw_error(f'(OperationError) Can not operate between different types '
                                  f'({i1.my_type}, {i2.my_type}).')

            if n_res is not None:
                if 0 < n_res < 1:
                    res = NUM(T_FLOAT, str(n_res))
                else:
                    res = NUM(T_INT, str(n_res))
            else:
                res = STR(s_res)

            return res

        elif operation.my_type == N_COMPOP:
            o1 = operation.get_v1()
            o2 = operation.get_v2()

            o1 = self.solve_icognite(o1)
            o2 = self.solve_icognite(o2)

            i1 = o1.syn_obj
            i2 = o2.syn_obj

            if o1.my_type == N_NUM and o2.my_type == N_NUM:
                i1 = int(i1) if o1.syn_class == T_INT else float(i1)
                i2 = int(i2) if o2.syn_class == T_INT else float(i2)

                if operation.op == GREATER:
                    if i1 > i2:
                        return BL('true')
                    else:
                        return BL('false')

                elif operation.op == SMALLER:
                    if i1 < i2:
                        return BL('true')
                    else:
                        return BL('false')

                elif operation.op == GR_OR_EQ:
                    if i1 >= i2:
                        return BL('true')
                    else:
                        return BL('false')

                elif operation.op == SM_OR_EQ:
                    if i1 <= i2:
                        return BL('true')
                    else:
                        return BL('false')

            if operation.op == EQUALS:
                if i1 == i2:
                    return BL('true')
                else:
                    return BL('false')

            elif operation.op == DIFFERENT:
                if i1 != i2:
                    return BL('true')
                else:
                    return BL('false')

            else:
                ERROR.throw_error(f'(OperationError) Can not perform "size type" comparison between '
                                  f'{o1.my_type} and {o2.my_type}, only between INTs')

        elif operation.my_type == N_BYLOG:
            o1 = operation.get_v1()
            o2 = operation.get_v2()

            o1 = self.solve_icognite(o1)
            o2 = self.solve_icognite(o2)

            i1 = o1.syn_obj
            i2 = o2.syn_obj

            if o1.my_type == N_BOOL and o2.my_type == N_BOOL:
                if operation.op == AND:
                    if i1 == 'true' and i2 == 'true':
                        return BL('true')
                    else:
                        return BL('false')

                elif operation.op == OR:
                    if i1 == 'true' or i2 == 'true':
                        return BL('true')
                    else:
                        return BL('false')
            else:
                ERROR.throw_error(f'(OperationError) Can only perform "logic operations" between booleans '
                                  f'tried to operate : ({o1.my_type}, {o2.my_type})')

        elif operation.my_type == N_ARR_ACCESS:
            ac_key = operation.get_key()
            memory_address = SOLID_DATA.get(ac_key)
            if memory_address is not None:
                indexes = operation.get_indexes()
                address_pointer = SOLID_DATA[ac_key]
                for i in indexes:
                    address_pointer = self.scarve_array(address_pointer, i)

                if address_pointer.my_type == N_ARRAY:
                    return self.generate_clone(address_pointer)
                return address_pointer
            else:
                ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {ac_key}, declare this '
                                  f'variable first!')

        elif operation.my_type == N_TO_OP:
            o1 = operation.get_v1()
            o2 = operation.get_v2()

            o1 = self.solve_icognite(o1)
            o2 = self.solve_icognite(o2)

            if o1.my_type == N_NUM and o2.my_type == N_NUM:
                if o1.syn_class == T_INT and o2.syn_class == T_INT:
                    i1 = int(o1.syn_obj)
                    i2 = int(o2.syn_obj)
                    arr = ARR()
                    for i in range(i1, i2+1):
                        arr.add_to_node_list(NUM(T_INT, str(i)))
                    return arr
                else:
                    ERROR.throw_error(f'(OperationError) TO operation can only take INT and INT as parameter. Took '
                                      f'{o1.my_type} and {o2.my_type} instead.')
            else:
                ERROR.throw_error(f'(OperationError) TO operation can only take INT and INT as parameter. Took '
                                  f'{o1.my_type} and {o2.my_type} instead.')

        elif operation.my_type == N_NOT_OP:
            i2 = operation.get_v2()
            i2 = self.solve_icognite(i2)

            if i2.my_type == N_BOOL:
                i2 = i2.syn_obj
                if i2 == 'true':
                    res = 'false'
                elif i2 == 'false':
                    res = 'true'

                res = lexer.set_tokens(lexer.lexate(res))[0]
                return res
            else:
                ERROR.throw_error(f'(OperationError) Can not deny non boolean values. (tried to deny {i2.my_type})')

        elif operation.my_type == N_ARR_SIZE:
            ad_type = operation.get_v2()
            if ad_type.my_type == N_KEY:
                ac_key = ad_type.syn_obj
                memory_address = SOLID_DATA.get(ac_key)
                if memory_address is not None:
                    if memory_address.my_type == N_ARRAY:
                        return NUM(T_INT, str(len(memory_address.get_node_list())))
                    else:
                        ERROR.throw_error(f'(OperationError) Size operator takes only arrays as parameter. Took '
                                          f'{memory_address.my_type} instead.')
                else:
                    ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {ac_key}, declare this '
                                      f'variable first!')

            elif ad_type.my_type == N_ARR_ACCESS:
                ac_key = ad_type.get_key()
                memory_address = SOLID_DATA.get(ac_key)
                if memory_address is not None:
                    indexes = ad_type.get_indexes()
                    address_pointer = SOLID_DATA[ac_key]
                    for i in indexes:
                        address_pointer = self.scarve_array(address_pointer, i)

                    if address_pointer.my_type == N_ARRAY:
                        return NUM(T_INT, str(len(address_pointer.get_node_list())))
                    else:
                        ERROR.throw_error(f'(OperationError) Size operator takes only arrays as parameter. Took '
                                          f'{memory_address.my_type} instead.')
                else:
                    ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {ac_key}, declare this '
                                      f'variable first!')
            else:
                ERROR.throw_error(f'(OperationError) Size operator takes only arrays as parameter. Took '
                                  f'{ad_type.my_type} instead.')

        elif operation.my_type == N_C_READ:
            i1 = self.solve_icognite(operation.get_v2())
            return STR(input(i1.syn_obj))

        elif operation.my_type == N_STRINGFY:
            i1 = self.solve_icognite(operation.get_v2())
            return STR(i1.syn_obj)

        elif operation.my_type == N_NUMFY:
            i1 = self.solve_icognite(operation.get_v2())
            if i1.my_type == N_STR:
                obj = i1.syn_obj
                if obj.isnumeric():
                    return NUM(T_INT, obj)
                else:
                    ERROR.throw_error(f'(TypeError) "int" operator requires numeric only strings as parameter, you gave '
                                      f'"{obj}" instead.')
            else:
                ERROR.throw_error(f'(OperationError) "int" operator takes only strings as parameter.'
                                  f' Took {i1.my_type} instead.')

        elif operation.my_type == N_PARBLOCK:
            for each in operation.get_node_array():
                res = self.solve_exp(each)  # REVER DEPOIS PARA A IMPLEMENTAÇÃO DE FN()
                return res

        elif operation.my_type in N_STR + N_NUM + N_BOOL + N_ARRAY + N_NULL:
            return operation

        elif operation.my_type == N_KEY:
            key = operation.syn_obj
            if SOLID_DATA.get(key) is not None:
                if SOLID_DATA[key].my_type == N_ARRAY:
                    return self.generate_clone(SOLID_DATA[key])
                else:
                    return SOLID_DATA[key]
            else:
                ERROR.throw_error(f'(MemoryError) Tried to access nonexistent memory: {operation.syn_obj}, declare this '
                                  f'variable first!')

    def solve_icognite(self, i):
        if i.my_type == N_KEY:
            if SOLID_DATA.get(i.syn_obj) is not None:
                return SOLID_DATA[i.syn_obj]
            else:
                ERROR.throw_error(
                    f'(MemoryError) Tried to access nonexistent memory: {i.syn_obj}, declare this '
                    f'variable first!')

        elif i.my_type == N_BINARYOP or i.my_type == N_COMPOP or i.my_type == N_PARBLOCK or i.my_type == N_NOT_OP or \
                i.my_type == N_ARR_SIZE or i.my_type == N_ARR_ACCESS or i.my_type == N_C_READ or \
                i.my_type == N_STRINGFY or i.my_type == N_BYLOG:
            return self.solve_exp(i)
        else:
            return i

    def scarve_array(self, array, index, mod=None, element=None):
        if array.my_type == N_ARRAY:
            c_list = array.get_node_list()
            index = self.solve_icognite(index)
            if index.my_type == N_NUM and index.syn_class == T_INT:
                index = int(index.syn_obj)
                max_index = len(c_list)-1
                if mod == 'add':
                    if -1 < index <= max_index:
                        c_list[index] = element
                    elif index > max_index:
                        it = index - max_index
                        for i in range(it):
                            if i == it-1:
                                c_list.append(element)
                            else:
                                c_list.append(NL())
                    else:
                        ERROR.throw_error(f'(AccessError) Index out of array bounds! Only positive values '
                                          f'are accepted in assignment.')

                elif mod == 'del':
                    if -1 < index <= max_index:
                        c_list.pop(index)
                    else:
                        ERROR.throw_error(f'(AccessError) Index out of array bounds! Only values from '
                                          f'0 to array size -1 are accepted for reading.')
                else:
                    if -1 < index <= max_index:
                        return c_list[index]
                    else:
                        ERROR.throw_error(f'(AccessError) Index out of array bounds! Only values from '
                                          f'0 to array size -1 are accepted for reading.')
            else:
                ERROR.throw_error(f'(TypeError) Array requires INTs as indexes, you gave '
                                  f'"{index.syn_class}" instead.')
        else:
            ERROR.throw_error(f'(TypeError) Tried to access index of non array object ({array.my_type}).')

    def generate_clone(self, n_array):
        node_list = n_array.get_node_list()
        clone = ARR()
        for each in node_list:
            if each.my_type == N_ARRAY:
                s_clone = ARR()
                s_clone.set_node_list(each.get_node_list().copy())
                clone.add_to_node_list(self.generate_clone(s_clone))
            else:
                clone.add_to_node_list(each)
        return clone
