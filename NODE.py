from DEPENDENCIES import *


# ---- NODES ----

class NODE:
    def __init__(self, s_type='NODE'):
        self.my_type = s_type
        self.syn_obj = 'null'
        self.syn_class = T_NULL

        self.line = 0
        self.colon = 0

    def self_write(self):
        return 'generic'

    def write_to_console(self):
        print(self.syn_obj, end='')


class NUM(NODE):
    def __init__(self, syn_class, syn_obj):
        super().__init__(N_NUM)
        self.syn_obj = syn_obj
        self.syn_class = syn_class

    def self_write(self):
        return f'{self.my_type} ({self.syn_class}): {self.syn_obj}'


class STR(NODE):
    def __init__(self, syn_obj):
        super().__init__(N_STR)
        self.syn_obj = syn_obj
        self.syn_class = T_STRING

    def self_write(self):
        return f'{self.my_type}: {self.syn_obj}'


class BL(NODE):
    def __init__(self, syn_obj):
        super().__init__(N_BOOL)
        self.syn_obj = syn_obj
        self.syn_class = T_BOOL

    def self_write(self):
        return f'{self.my_type}: {self.syn_obj}'


class OPER(NODE):
    def __init__(self, syn_obj):
        super().__init__(N_OPER)
        self.syn_obj = syn_obj
        self.syn_class = T_OPERATOR

    def self_write(self):
        return f'{self.my_type}: {self.syn_obj}'


class SYM(NODE):
    def __init__(self, syn_obj):
        super().__init__(N_SYM)
        self.syn_obj = syn_obj
        self.syn_class = T_SYMBOL

    def self_write(self):
        return f'{self.my_type}: {self.syn_obj}'


class K(NODE):
    def __init__(self, syn_obj):
        super().__init__(N_KEY)
        self.syn_obj = syn_obj
        self.syn_class = T_KEY

    def self_write(self):
        return f'{self.my_type}: {self.syn_obj}'


class NL(NODE):
    def __init__(self):
        super().__init__(N_NULL)
        self.syn_obj = 'null'
        self.syn_class = T_NULL

    def self_write(self):
        return f'{self.my_type}: {self.syn_obj}'


class ARR(NODE):
    def __init__(self):
        super().__init__(N_ARRAY)
        self._node_list = []

    def self_write(self):
        elements = ''
        for e in self._node_list:
            elements += e.self_write() + ','
        return '-l ' + elements + ' l-'

    def get_node_list(self):
        return self._node_list

    def set_node_list(self, nlist):
        self._node_list = nlist

    def add_to_node_list(self, item):
        self._node_list.append(item)

    def set_element(self, index, node):
        self._node_list[index] = node

    def write_to_console(self):
        print('[', end='')
        bound = len(self._node_list)
        for i in range(bound):
            self._node_list[i].write_to_console()
            if i < bound-1:
                print(',', end=' ')
        print(']', end='')


class DECLARATION(NODE):
    def __init__(self, reserve):
        super().__init__(N_DECLARATION)
        self._key = None            # string label
        self._reserve = reserve     # string label

    def self_write(self):
        return f'~ {self.my_type} : {self._key}'

    def set_key(self, key):
        self._key = key

    def get_key(self):
        if self._key is not None:
            return self._key

    def get_reserve(self):
        return self._reserve


class DELETATION(NODE):
    def __init__(self):
        super().__init__(N_DELETATION)
        self._value = None            # NODE (key, arraccess) for memory label

    def self_write(self):
        return f'~ {self.my_type} : {self._value}'

    def set_value(self, key):
        self._value = key

    def get_value(self):
        if self._value is not None:
            return self._value


class ASSIGNMENT(NODE):
    def __init__(self, key):
        super().__init__(N_ASSIGNMENT)
        self._key = key             # NODE (expread) for memory label
        self._value = None          # NODE (str, num, key, null, array, operations) for value to save

    def self_write(self):
        return f'~ {self.my_type} : {self._key} <- {self._value.self_write()}'

    def get_key(self):
        return self._key

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


class CONSOLEWRITE(NODE):
    def __init__(self):
        super().__init__(N_C_WRITE)
        self._value = None

    def self_write(self):
        return f'~ {self.my_type} : {self._value.self_write()}'

    def get_value(self):
        return self._value

    def set_value(self, key):
        self._value = key


class CONSOLEREAD(NODE):
    def __init__(self):
        super().__init__(N_C_READ)
        self.op = 'read'
        self._value2 = None

    def self_write(self):
        return f'~ {self.op} <- ({self._value2.self_write()})'

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v2(self, value):
        self._value2 = value


class EXPREAD(NODE):
    def __init__(self, key):
        super().__init__(N_EXP_READ)
        self._key = key             # string label

    def self_write(self):
        return f'~ {self.my_type} : {self._key.self_write()}'

    def set_key(self, key):
        self._key = key

    def get_key(self):
        if self._key is not None:
            return self._key


class ARRACCESS(NODE):
    def __init__(self, key, indexes):
        super().__init__(N_ARR_ACCESS)
        self._key = key
        self.indexes = indexes

    def self_write(self):
        return f'~ {self.my_type} : {self._key.self_write()} [{self.indexes}]'

    def get_key(self):
        return self._key

    def get_indexes(self):
        return self.indexes.get_node_list()


class BYNARYOP(NODE):
    def __init__(self, op):
        super().__init__(N_BINARYOP)
        self.op = op
        self._value1 = None
        self._value2 = None
        self.tk_obj = 'None'

    def self_write(self):
        return f'~ {self.op} : ({self._value1.self_write()}, {self._value2.self_write()})'

    def get_v1(self):
        if self._value1 is not None:
            return self._value1

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v1(self, value):
        self._value1 = value

    def set_v2(self, value):
        self._value2 = value


class COMPOP(NODE):
    def __init__(self, op):
        super().__init__(N_COMPOP)
        self.op = op
        self._value1 = None
        self._value2 = None
        self.tk_obj = 'None'

    def self_write(self):
        return f'~ {self.op} : ({self._value1.self_write()}, {self._value2.self_write()})'

    def get_v1(self):
        if self._value1 is not None:
            return self._value1

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v1(self, value):
        self._value1 = value

    def set_v2(self, value):
        self._value2 = value


class BYNARYLOGIC(NODE):
    def __init__(self, op):
        super().__init__(N_BYLOG)
        self.op = op
        self._value1 = None
        self._value2 = None

    def self_write(self):
        return f'~ {self.op} : ({self._value1.self_write()}, {self._value2.self_write()})'

    def get_v1(self):
        if self._value1 is not None:
            return self._value1

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v1(self, value):
        self._value1 = value

    def set_v2(self, value):
        self._value2 = value


class NOTOP(NODE):
    def __init__(self):
        super().__init__(N_NOT_OP)
        self.op = 'not'
        self._value2 = None
        self.tk_obj = 'None'

    def self_write(self):
        return f'~ {self.op} : ({self._value2.self_write()})'

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v2(self, value):
        self._value2 = value


class CONDSTATEMENT(NODE):
    def __init__(self, layer):
        super().__init__(N_COND_STATEMENT)
        self.layer = layer
        self._value = None
        self._exe_block = None

    def self_write(self):
        return f'~ {self.my_type} : {self._value.self_write()} -> {self._exe_block.self_write()}'

    def get_value(self):
        return self._value

    def set_value(self, operation):
        self._value = operation

    def get_exeblock(self):
        return self._exe_block

    def set_exeblock(self, block):
        self._exe_block = block


class WLOOP(NODE):
    def __init__(self):
        super().__init__(N_WHILE_LOOP)
        self._value = None
        self._exe_block = None

    def self_write(self):
        return f'~ {self.my_type} : {self._value.self_write()} -> {self._exe_block.self_write()}'

    def get_value(self):
        return self._value

    def set_value(self, operation):
        self._value = operation

    def get_exeblock(self):
        return self._exe_block

    def set_exeblock(self, block):
        self._exe_block = block


class FLOOP(NODE):
    def __init__(self):
        super().__init__(N_FOR_LOOP)
        self._value = None
        self._exe_block = None

    def self_write(self):
        return f'~ {self.my_type} : {self._value.self_write()} -> {self._exe_block}'

    def get_value(self):
        return self._value

    def set_value(self, op):
        self._value = op

    def get_exeblock(self):
        return self._exe_block

    def set_exeblock(self, block):
        self._exe_block = block


class FROMOP(NODE):
    def __init__(self):
        super().__init__('from')
        self.op = 'from'
        self._value1 = None
        self._value2 = None

    def self_write(self):
        return f'({self._value1.self_write()} <-each- {self._value2.self_write()})'

    def get_v1(self):
        if self._value1 is not None:
            return self._value1

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v1(self, value):
        self._value1 = value

    def set_v2(self, value):
        self._value2 = value


class PARBLOCK(NODE):
    def __init__(self):
        super().__init__(N_PARBLOCK)
        self._nodeArray = []

    def self_write(self):
        elements = ''
        for e in self._nodeArray:
            elements += e.self_write() + ','
        return '-p' + elements + 'p-'

    def get_node_array(self):
        return self._nodeArray

    def set_node_array(self, array):
        self._nodeArray = array

    def add_to_node_array(self, e):
        self._nodeArray.append(e)


class CODEBLOCK(NODE):
    def __init__(self):
        super().__init__('codeblock')
        self._block = None

    def self_write(self):
        elements = ''
        for e in self._block:
            elements += e.self_write() + ','
        return '-B' + elements + 'B-'

    def get_block(self):
        return self._block

    def set_block(self, block):
        self._block = block


class FUNDEC(NODE):
    def __init__(self):
        super().__init__(N_FUN_DEC)
        self._key = None
        self.parameters = None
        self._exe_block = None

    def self_write(self):
        return f'~ {self.my_type} {self._key} ({self.parameters.self_write()}) -> {self._exe_block}'

    def get_key(self):
        return self._key

    def set_key(self, k):
        self._key = k

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, parblock):
        self.parameters = parblock

    def get_exeblock(self):
        return self._exe_block

    def set_exeblock(self, block):
        self._exe_block = block


class FUNCALL(NODE):
    def __init__(self, key, parameters):
        super().__init__(N_FUN_CALL)
        self._key = key            # string label
        self.parameters = parameters      # parblock

    def self_write(self):
        return f'~ {self.my_type} : {self._key}({self.parameters.self_write()})'

    def get_key(self):
        return self._key

    def set_key(self, k):
        self._key = k

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, parblock):
        self.parameters = parblock


class FUN(NODE):
    def __init__(self, paramaters, block):
        super().__init__(N_FUN)
        self.parameters = paramaters
        self._exe_block = block

    def self_write(self):
        return f'~ {self.my_type} ({self.parameters.self_write()}) -> {self._exe_block}'

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, parblock):
        self.parameters = parblock

    def get_exeblock(self):
        return self._exe_block

    def set_exeblock(self, block):
        self._exe_block = block


class STRINGFY(NODE):
    def __init__(self):
        super().__init__(N_STRINGFY)
        self.op = 'stringfy'
        self._value2 = None
        self.tk_obj = 'None'

    def self_write(self):
        return f'~ {self.op} : ({self._value2.self_write()})'

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v2(self, value):
        self._value2 = value


class NUMFY(NODE):
    def __init__(self):
        super().__init__(N_NUMFY)
        self.op = 'numfy'
        self._value2 = None
        self.tk_obj = 'None'

    def self_write(self):
        return f'~ {self.op} : ({self._value2.self_write()})'

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v2(self, value):
        self._value2 = value


class ARRSIZE(NODE):
    def __init__(self):
        super().__init__(N_ARR_SIZE)
        self.op = 'arrsize'
        self._value2 = None
        self.tk_obj = 'None'

    def self_write(self):
        return f'~ {self.op} : ({self._value2.self_write()})'

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v2(self, value):
        self._value2 = value


class TOOP(NODE):
    def __init__(self):
        super().__init__(N_TO_OP)
        self.op = 'to'
        self._value1 = None
        self._value2 = None

    def self_write(self):
        return f'~ {self._value1.self_write()} {self.op} {self._value2.self_write()}'

    def get_v1(self):
        if self._value1 is not None:
            return self._value1

    def get_v2(self):
        if self._value2 is not None:
            return self._value2

    def set_v1(self, value):
        self._value1 = value

    def set_v2(self, value):
        self._value2 = value


# ----- STRUCTURE NODES -----

class AST:
    def __init__(self):
        self.my_type ='AST'
        self.tree = []

    def self_write(self):
        elements = ''
        elements += 'AST\n:'
        for each in self.tree:
            elements += '\t'
            elements += each.self_write()
            elements += ';\n'
        elements += 'END_AST'

        return elements
