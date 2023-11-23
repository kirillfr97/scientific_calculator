from typing import List

max_digit_count = 12


class OperationList:
    CL = 'CL'
    CL_ALL = 'CL_ALL'
    DEL = 'DEL'

    TOTAL = 'TOTAL'
    SIGN = 'SIGN'

    SUM = 'SUM'
    DIFF = 'DIFF'
    MULTI = 'MULTI'
    DIV = 'DIV'
    MOD = 'MOD'
    SQRT = 'SQRT'
    POWER2 = 'POWER2'
    POWER3 = 'POWER3'
    REVERSE = 'REVERSE'
    PI = 'PI'
    COS = 'COS'
    SIN = 'SIN'
    TAN = 'TAN'
    E = 'E'
    ACOS = 'ACOS'
    ASIN = 'ASIN'
    ATAN = 'ATAN'
    LN = 'LN'
    EXP = 'EXP'
    EXP10 = 'EXP10'
    SEC = 'SEC'
    CSC = 'CSC'
    LOG2 = 'LOG2'
    LOG10 = 'LOG10'
    FACTORIAL = 'FACTORIAL'
    MODUL = 'MODUL'


OnTotalOperations: List[str] = [
    OperationList.SUM,
    OperationList.DIFF,
    OperationList.MULTI,
    OperationList.DIV,
    OperationList.MOD,
    OperationList.EXP,
]
