from pathlib import Path
from os.path import join
from typing import Callable, List
from collections import namedtuple

from PyQt6.QtGui import QFont, QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLCDNumber, QGridLayout

from calculator import max_digit_count, OperationList
from calculator.calculator import Calculator

current_directory = str(Path(__file__).parent.absolute())

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
        self.setStyleSheet('background-color:' + bg_color)
        self.clicked.connect(command)

    def description(self) -> str:
        return self._description


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()

        self.setWindowTitle('Calculator')
        self.setWindowIcon(QIcon(join(current_directory, 'images', 'icon.png')))

        # noinspection PyArgumentList
        self.numpad_list = [
            CalcButton('CE', OperationList.CL, self._clear_input_clicked),
            CalcButton('C', OperationList.CL_ALL, self._clear_total_clicked),
            CalcButton(chr(9003), OperationList.DEL, self._delete_clicked),
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

        # noinspection PyArgumentList
        self.scientific_list = [
            CalcButton('\u221Ax', OperationList.SQRT, self._operation_clicked),
            CalcButton('x' + chr(178), OperationList.POWER2, self._operation_clicked),
            CalcButton('x' + chr(179), OperationList.POWER3, self._operation_clicked),

            CalcButton('1/x', OperationList.REVERSE, self._operation_clicked),
            CalcButton('|x|', OperationList.MODUL, self._operation_clicked),
            CalcButton('n!', OperationList.FACTORIAL, self._operation_clicked),

            CalcButton('cos', OperationList.COS, self._operation_clicked),
            CalcButton('sin', OperationList.SIN, self._operation_clicked),
            CalcButton('tan', OperationList.TAN, self._operation_clicked),

            CalcButton('acos', OperationList.ACOS, self._operation_clicked),
            CalcButton('asin', OperationList.ASIN, self._operation_clicked),
            CalcButton('atan', OperationList.ATAN, self._operation_clicked),

            CalcButton(chr(960), OperationList.PI, self._operation_clicked),
            CalcButton('sec', OperationList.SEC, self._operation_clicked),
            CalcButton('x' + '\u207F', OperationList.EXP, self._operation_clicked),

            CalcButton('e', OperationList.E, self._operation_clicked),
            CalcButton('csc', OperationList.CSC, self._operation_clicked),
            CalcButton('10' + '\u207F', OperationList.EXP10, self._operation_clicked),

            CalcButton('ln', OperationList.LN, self._operation_clicked),
            CalcButton('log2', OperationList.LOG2, self._operation_clicked),
            CalcButton('log10', OperationList.LOG10, self._operation_clicked),
        ]

        self._initUI()

    def _initUI(self):
        common_calc = QAction('Ordinary', self)
        common_calc.setStatusTip('Switch to ordinary calculator')
        common_calc.triggered.connect(self._calc2common)

        scientific_calc = QAction('Scientific', self)
        scientific_calc.setStatusTip('Switch to scientific calculator')
        scientific_calc.triggered.connect(self._calc2scientific)

        calculator = self.menuBar().addMenu('Mode')
        calculator.addAction(common_calc)
        calculator.addAction(scientific_calc)

        self.lcd_number = QLCDNumber(max_digit_count)
        self.lcd_number.setMinimumSize(350, 80)

        self.numpad = QWidget()
        self.numpad_grid = QGridLayout()
        self.numpad.setLayout(self.numpad_grid)

        self.scientific = QWidget()
        self.scientific_grid = QGridLayout()
        self.scientific.setLayout(self.scientific_grid)

        numpad_layout = QVBoxLayout()
        numpad_layout.addWidget(self.lcd_number)
        numpad_layout.addWidget(self.numpad)

        central_layout = QHBoxLayout()
        central_layout.addLayout(numpad_layout)
        central_layout.addWidget(self.scientific)

        central_wdg = QWidget()
        central_wdg.setLayout(central_layout)

        def create_button_grid(button_list: List[CalcButton], layout: QGridLayout, columns: int):
            rows = len(button_list) // columns
            for row in range(rows):
                for column in range(columns):
                    item = button_list[row * columns + column]
                    layout.addWidget(
                        Button(
                            text=item.text,
                            description=item.description,
                            checkable=item.checkable,
                            command=item.command,
                            bg_color=item.bg_color
                        ), row, column
                    )

        create_button_grid(self.numpad_list, self.numpad_grid, 4)
        create_button_grid(self.scientific_list, self.scientific_grid, 3)

        self.setCentralWidget(central_wdg)
        self.scientific.hide()

    def _calc2common(self):
        self.scientific.hide()

    def _calc2scientific(self):
        self.scientific.show()

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
