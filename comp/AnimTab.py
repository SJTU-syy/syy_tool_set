from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


# Anim分页
class AnimTab(QWidget):
    def __init__(self, parent=None):
        super(AnimTab, self).__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Anim功能说明"))
        layout.addWidget(QPushButton("Anim按钮1"))
        layout.addWidget(QPushButton("Anim按钮2"))
        self.setLayout(layout)