from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from comp import tabs


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
        self.add_tabs()

    # 添加分页
    def add_tabs(self):
        self.tab_widget.addTab(tabs.BodyTab(), "Body")
        self.tab_widget.addTab(tabs.FacialTab(), "Facial")
        self.tab_widget.addTab(tabs.AnimTab(), "Anim")
        self.tab_widget.addTab(tabs.ToolTab(), "Tool")
        self.tab_widget.addTab(tabs.SettingTab(), "Setting")

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
