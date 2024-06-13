# ---- OPEN FILE ----

math_op = ['=', '+', '-', '/', '*']
logic_op = ['!', '>', '<', '!=', '==', '>=', '<=', '&&', '||']
operators = math_op + logic_op + ['str', 'int', 'from', 'to', 'size', 'read']

punctuations = [',', ';', ':', '.', '?']
groupers = ['(', ')', '[', ']', '{', '}']

symbols = punctuations + groupers + ['\n']

specialChars = operators + symbols

key_words = ('var', 'arr', 'del', 'if', 'else', 'elsif', 'fn', 'for',
             'while', 'write', 'true', 'false', 'str', 'from', 'to', 'size',
             'read', 'str')

SOLID_DATA = {}

# ---- TOKEN TYPES ----

T_KEY = 'key'
T_SYMBOL = 'symbol'
T_STRING = 'string'
T_INT = 'int'
T_FLOAT = 'float'
T_OPERATOR = 'operator'
T_BOOL = 'bool'
T_NULL = 'null'

# ---- OPERATION TYPES ----

SUM = 'sum'
SUB = 'sub'
MUL = 'mul'
DIV = 'div'

EQUALS = 'equals'
DIFFERENT = 'different'
GREATER = 'greater'
SMALLER = 'smaller'
GR_OR_EQ = 'gr_or_eq'
SM_OR_EQ = 'sm_or_eq'
NOT = 'not'

AND = 'and'
OR = 'or'

# ---- NODE TYPES ----

N_NUM = 'NUM'
N_STR = 'STRING'
N_BOOL = 'BOOL'
N_OPER = 'OPER'
N_SYM = 'SYMBOL'
N_KEY = 'KEY'
N_NULL = 'NULL'
N_ARRAY = 'ARRAY'
N_FUN = 'FUNCTION'
N_DECLARATION = 'declaration'
N_ASSIGNMENT = 'assignment'
N_C_WRITE = 'console-write'
N_C_READ = 'console-read'
N_PARBLOCK = "n_parblock"
N_BINARYOP = "n_binaryop"
N_COMPOP = "n_compop"
N_BYLOG = 'n_bylog'
N_DELETATION = 'n_deletation'
N_EXP_READ = 'n_exp_read'
N_ARR_ACCESS = 'n_arr_acc'
N_NOT_OP = 'n_not_op'
N_ARR_SIZE = 'n_arr_size'
N_COND_STATEMENT = 'cond-statement'
N_WHILE_LOOP = 'while-loop'
N_FOR_LOOP = 'for-loop'
N_FUN_DEC = 'n_fun_dec'
N_FUN_CALL = 'n_fun_call'
N_STRINGFY = 'n_strigfy'
N_NUMFY = 'n_numfy'
N_TO_OP = 'n_to-op'
