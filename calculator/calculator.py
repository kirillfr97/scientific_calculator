import math
from typing import Optional, Union

from calculator import max_digit_count, OperationList, OnTotalOperations


def is_integer(value: float) -> bool:
    return value % 1 == 0


def number2str(number: Union[float, int]) -> str:
    if is_integer(number):
        return str(int(number))[:max_digit_count]
    else:
        return str(number)[:max_digit_count]


class Calculator:

    def __init__(self):
        #
        self._total: float = 0
        #
        self._memory: list = []
        #
        self._current: str = '0'
        #
        self._operation: str = ''
        #
        self._await_input: bool = True
        #
        self._await_result: bool = True

    def _valid_function(self, operation: Optional[str] = None):
        current = float(self._current)
        operation = self._operation if operation is None else operation
        if operation == OperationList.SUM:
            self._total += current
        if operation == OperationList.DIFF:
            self._total -= current
        if operation == OperationList.MULTI:
            self._total *= current
        if operation == OperationList.DIV:
            if current == 0:
                raise ZeroDivisionError
            self._total /= current
        if operation == OperationList.MOD:
            self._total %= current

        if operation == OperationList.REVERSE:
            if current == 0:
                raise ZeroDivisionError
            self._current = number2str(1 / current)
        if operation == OperationList.POWER2:
            self._current = number2str(math.pow(current, 2))
        if operation == OperationList.SQRT:
            self._current = number2str(math.sqrt(current))

    def number_enter(self, value: str) -> str:
        if self._current == '0' and value == '0':
            return self._current

        if self._await_input:
            self._current = value if value != '.' else '0.'
            self._await_input = False
        else:
            if value == '.' and value in self._current:
                return self._current

            if len(self._current) + 1 <= max_digit_count:
                self._current += value

        return self._current

    def operation_enter(self, operation: str):
        try:
            self._await_input = True
            if operation not in OnTotalOperations:
                self._valid_function(operation)
                return self._current

            if self._await_result:
                self._await_result = False
                self._total = float(self._current)
            else:
                self._valid_function()
                self._current = number2str(self._total)
            self._operation = operation
        except ZeroDivisionError:
            self.clear_input()
            return 'Err'

        return self._current

    def total_enter(self):
        self._valid_function()
        self._current = number2str(self._total)
        self._total = 0.0
        self._operation = ''
        self._await_input = True
        self._await_result = True

        return self._current

    def sign_changed(self) -> str:
        if self._current == '0':
            return self._current

        if self._current[0] != '-':
            self._current = '-' + self._current
        else:
            self._current = self._current[1:]

        return self._current

    def delete_last(self) -> str:
        self._current = self._current[:-1]
        if self._current in ['0', '', '-']:
            self._current = '0'
            self._await_input = True

        return self._current

    def clear_input(self):
        self._current = '0'
        self._await_input = True

    def clear_total(self):
        self.clear_input()
        self._total = 0.0
        self._operation = ''
        self._await_result = True
        self._memory.clear()
