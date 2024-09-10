import sys
from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

# 获取Maya主窗口的指针
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QMainWindow)

# 创建一个主窗口类
class SimpleMayaWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SimpleMayaWindow, self).__init__(parent)
        self.setWindowTitle("多分页界面")
        self.setGeometry(100, 100, 600, 400)

        # 创建一个QTabWidget
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # 添加五个分页
        self.add_body_tab()
        self.add_facial_tab()
        self.add_anim_tab()
        self.add_tool_tab()
        self.add_setting_tab()

    # 添加Body分页
    def add_body_tab(self):
        body_tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Body功能说明"))
        layout.addWidget(QPushButton("Body按钮1"))
        layout.addWidget(QPushButton("Body按钮2"))
        body_tab.setLayout(layout)
        self.tab_widget.addTab(body_tab, "Body")

    # 添加Facial分页
    def add_facial_tab(self):
        facial_tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Facial功能说明"))
        layout.addWidget(QPushButton("Facial按钮1"))
        layout.addWidget(QPushButton("Facial按钮2"))
        facial_tab.setLayout(layout)
        self.tab_widget.addTab(facial_tab, "Facial")

    # 添加Anim分页
    def add_anim_tab(self):
        anim_tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Anim功能说明"))
        layout.addWidget(QPushButton("Anim按钮1"))
        layout.addWidget(QPushButton("Anim按钮2"))
        anim_tab.setLayout(layout)
        self.tab_widget.addTab(anim_tab, "Anim")

    # 添加Tool分页
    def add_tool_tab(self):
        tool_tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tool功能说明"))
        layout.addWidget(QPushButton("Tool按钮1"))
        layout.addWidget(QPushButton("Tool按钮2"))
        tool_tab.setLayout(layout)
        self.tab_widget.addTab(tool_tab, "Tool")

    # 添加Setting分页
    def add_setting_tab(self):
        setting_tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Setting功能说明"))
        layout.addWidget(QPushButton("Setting按钮1"))
        layout.addWidget(QPushButton("Setting按钮2"))
        setting_tab.setLayout(layout)
        self.tab_widget.addTab(setting_tab, "Setting")

# 主函数
def main():
    # 创建QApplication实例
    app = QApplication.instance()
    if not app:
        app = QApplication([])

    # 获取Maya主窗口
    maya_main_window = get_maya_main_window()

    # 创建并显示窗口
    window = SimpleMayaWindow(parent=maya_main_window)
    window.show()

    # 进入应用程序主循环
    app.exec_()

# 运行主函数
if __name__ == "__main__":
    main()
