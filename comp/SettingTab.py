from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


# Setting分页
class SettingTab(QWidget):
    def __init__(self, parent=None):
        super(SettingTab, self).__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Setting功能说明"))
        layout.addWidget(QPushButton("Setting按钮1"))
        layout.addWidget(QPushButton("Setting按钮2"))
        self.setLayout(layout)