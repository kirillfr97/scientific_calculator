from PyQt6.QtWidgets import QApplication

import sys

from calculator.calculator_widget import MainWindow

app = QApplication(sys.argv)

main = MainWindow()
main.show()

app.exec()






