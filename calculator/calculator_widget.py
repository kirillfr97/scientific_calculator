from typing import Callable
from collections import namedtuple

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLCDNumber, QGridLayout

from calculator import max_digit_count, OperationList
from calculator.calculator import Calculator


CalcButton = namedtuple('CalcButton',
                        ['text', 'description', 'command', 'checkable', 'bg_color'],
                        defaults=[None, None, None, False, 'grey'])


class Button(QPushButton):
    def __init__(self, 
                 text: str, 
                 description: str, 
                 command: Callable, 
                 checkable: bool,
                 bg_color: str):
        super().__init__(text=text)

        self._description = description

        font = QFont('Helvetica', 18)
        font.setBold(True)
        self.setFont(font)
        self.setCheckable(checkable)
        self.setStyleSheet("background-color:" + bg_color)
        self.clicked.connect(command)

    def description(self) -> str:
        return self._description


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calculator')
        self.calculator = Calculator()

        self._initUI()

    def _initUI(self):
        self.lcd_number = QLCDNumber(max_digit_count)
        self.lcd_number.setMinimumSize(100, 90)
        self.control_grid = QGridLayout()

        central_layout = QVBoxLayout()
        central_layout.addWidget(self.lcd_number)
        central_layout.addLayout(self.control_grid)

        central_wdg = QWidget()
        central_wdg.setLayout(central_layout)

        # noinspection PyArgumentList
        btn_list = [
            CalcButton('%', OperationList.MOD, self._operation_clicked),
            CalcButton('CE', OperationList.CL, self._clear_input_clicked),
            CalcButton('C', OperationList.CL_ALL, self._clear_total_clicked),
            CalcButton(chr(9003), OperationList.DEL, self._delete_clicked),

            CalcButton('1/x', OperationList.REVERSE, self._operation_clicked),
            CalcButton('x' + chr(178), OperationList.POWER2, self._operation_clicked),
            CalcButton('\u221Ax', OperationList.SQRT, self._operation_clicked),
            CalcButton('/', OperationList.DIV, self._operation_clicked),

            CalcButton('7', '7', self._number_clicked),
            CalcButton('8', '8', self._number_clicked),
            CalcButton('9', '9', self._number_clicked),
            CalcButton('x', OperationList.MULTI, self._operation_clicked),

            CalcButton('4', '4', self._number_clicked),
            CalcButton('5', '5', self._number_clicked),
            CalcButton('6', '6', self._number_clicked),
            CalcButton('-', OperationList.DIFF, self._operation_clicked),

            CalcButton('1', '1', self._number_clicked),
            CalcButton('2', '2', self._number_clicked),
            CalcButton('3', '3', self._number_clicked),
            CalcButton('+', OperationList.SUM, self._operation_clicked),

            CalcButton(chr(177), OperationList.SIGN, self._sign_clicked),
            CalcButton('0', '0', self._number_clicked),
            CalcButton('.', '.', self._number_clicked),
            CalcButton('=', OperationList.TOTAL, self._total_clicked, bg_color='red'),
        ]

        columns = 4
        rows = len(btn_list) // columns
        for row in range(rows):
            for column in range(columns):
                item = btn_list[row * columns + column]
                self.control_grid.addWidget(
                    Button(
                        text=item.text,
                        description=item.description,
                        checkable=item.checkable,
                        command=item.command,
                        bg_color=item.bg_color
                    ), row, column
                )

        self.setCentralWidget(central_wdg)

    def _number_clicked(self):
        # noinspection PyTypeChecker
        sender: Button = self.sender()

        text = sender.description()
        value = self.calculator.number_enter(text)
        self.lcd_number.display(value)

    def _operation_clicked(self):
        # noinspection PyTypeChecker
        sender: Button = self.sender()

        text = sender.description()
        value = self.calculator.operation_enter(text)
        self.lcd_number.display(value)

    def _total_clicked(self):
        value = self.calculator.total_enter()
        self.lcd_number.display(value)

    def _sign_clicked(self):
        value = self.calculator.sign_changed()
        self.lcd_number.display(value)

    def _delete_clicked(self):
        value = self.calculator.delete_last()
        self.lcd_number.display(value)

    def _clear_input_clicked(self):
        self.lcd_number.display('0')
        self.calculator.clear_input()

    def _clear_total_clicked(self):
        self.lcd_number.display('0')
        self.calculator.clear_total()
