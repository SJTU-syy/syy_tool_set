import sys
from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

# 获取Maya主窗口的指针
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QMainWindow)

# 创建一个主窗口类，所有逻辑在这里面
class SimpleMayaWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SimpleMayaWindow, self).__init__(parent)
        # 设置窗口
        self.setWindowTitle("简单Maya PySide2窗口")
        self.setGeometry(100, 100, 300, 200)

        # 创建按钮
        self.button = QPushButton("点击我", self)
        self.button.setGeometry(100, 80, 100, 30)
        self.button.clicked.connect(self.show_message)



    # 按钮点击事件处理函数
    def show_message(self):
        QMessageBox.information(self, "消息", "你点击了按钮!")

# 主函数
def main():
    # 创建QApplication实例
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # 获取Maya主窗口
    maya_main_window = get_maya_main_window()

    # 创建并显示窗口
    window = SimpleMayaWindow(parent=maya_main_window)
    window.show()

    # 进入应用程序主循环，加的话MAYA会报错，但是可以发现后端数据是记录的。记得删掉
    # sys.exit(app.exec_())

# 运行主函数
if __name__ == "__main__":
    main()
