from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *




window = QWidget()
window.setWindowTitle(u"欢迎使用 PySide2 编写窗口")


def printHelloWorld(self):
    print("hello,world")

button = QPushButton("hello,world")
button.clicked.connect(printHelloWorld)

layout = QHBoxLayout()
layout.addWidget(button)
window.setLayout(layout)


window.show()