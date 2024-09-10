from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

# Facial分页
class FacialTab(QWidget):
    def __init__(self, parent=None):
        super(FacialTab, self).__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Facial功能说明"))
        layout.addWidget(QPushButton("Facial按钮1"))
        layout.addWidget(QPushButton("Facial按钮2"))
        self.setLayout(layout)