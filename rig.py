import os
import sys
import inspect

# 将当前脚本所在目录添加到环境变量中
current_frame = inspect.currentframe()
script_dir = os.path.dirname(os.path.abspath(inspect.getfile(current_frame)))
if script_dir not in sys.path:
    sys.path.append(script_dir)


def reload_modules(package_name):
    import pkgutil
    import importlib

    package = sys.modules.get(package_name)
    if package is None:
        raise ValueError(f"Package '{package_name}' is not loaded.")

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        if full_module_name in sys.modules:
            print(f"Reloading module '{full_module_name}'...")
            importlib.reload(sys.modules[full_module_name])
        else:
            print(f"Importing module '{full_module_name}'...")
            importlib.import_module(full_module_name)

# 最短也就缩成这4行了，老老实实导入吧
import comp
import func
reload_modules('comp')
reload_modules('func')

from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget
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