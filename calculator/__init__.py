from typing import List

max_digit_count = 12


class OperationList:
    CL = 'CL'
    CL_ALL = 'CL_ALL'
    DEL = 'DEL'

    TOTAL = 'TOTAL'
    SUM = 'SUM'
    DIFF = 'DIFF'
    MULTI = 'MULTI'
    DIV = 'DIV'
    MOD = 'MOD'
    SQRT = 'SQRT'
    POWER2 = 'POWER2'
    REVERSE = 'REVERSE'
    SIGN = 'SIGN'


OnTotalOperations: List[str] = [
    OperationList.SUM,
    OperationList.DIFF,
    OperationList.MULTI,
    OperationList.DIV,
    OperationList.MOD,
]
