# import sys
# import os
#
# # 将路径添加到sys.path,必须要有绝对路径,导一次就行,导入的代码不会动态更新
# sys.path.append(r'F:\Pycharm2024\pythonProject')

from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

import comp.BodyTab
import comp.FacialTab
import comp.AnimTab
import comp.ToolTab
import comp.SettingTab

# 重新加载模块,虽然看着蠢但是有用
import importlib
importlib.reload(comp.BodyTab)
importlib.reload(comp.FacialTab)
importlib.reload(comp.AnimTab)
importlib.reload(comp.ToolTab)
importlib.reload(comp.SettingTab)

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
        self.tab_widget.addTab(comp.BodyTab.BodyTab(), "Body")
        self.tab_widget.addTab(comp.FacialTab.FacialTab(), "Facial")
        self.tab_widget.addTab(comp.AnimTab.AnimTab(), "Anim")
        self.tab_widget.addTab(comp.ToolTab.ToolTab(), "Tool")
        self.tab_widget.addTab(comp.SettingTab.SettingTab(), "Setting")

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


# 运行主函数
if __name__ == "__main__":
    main()