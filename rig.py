import os
import sys
import inspect

from PySide2.QtCore import QSettings, QPoint, QSize

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

from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QMessageBox
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
        self.setWindowTitle("maya工具箱")
        self.setGeometry(100, 100, 400, 400)

        # 创建一个QTabWidget
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # 添加分页
        self.add_tabs()

        #创建菜单栏
        self.create_menu()

        # 恢复窗口的大小和位置
        self.read_settings()

        # 加载主题设置
        self.load_theme_setting()

    # 添加分页
    def add_tabs(self):
        self.tab_widget.addTab(comp.BodyTab.BodyTab(), "Body")
        self.tab_widget.addTab(comp.RigTab.RigTab(), "Rig")
        self.tab_widget.addTab(comp.FacialTab.FacialTab(), "Facial")
        self.tab_widget.addTab(comp.AnimTab.AnimTab(), "Anim")
        self.tab_widget.addTab(comp.NameTab.NameTab(), "Name")
        self.tab_widget.addTab(comp.SettingTab.SettingTab(), "Setting")


    # 创建菜单栏
    def create_menu(self):
        # 创建菜单栏
        menubar = self.menuBar()

        # 创建 'Windows' 菜单
        windows_menu = menubar.addMenu('Windows')

        # 添加 Windows 菜单项
        open_body_tab_action = QAction('Open Body Tab', self)
        open_body_tab_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        windows_menu.addAction(open_body_tab_action)

        open_facial_tab_action = QAction('Open Facial Tab', self)
        open_facial_tab_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        windows_menu.addAction(open_facial_tab_action)

        # 创建 'Theme' 菜单
        theme_menu = menubar.addMenu('Theme')

        # 添加 Theme 菜单项
        one_theme_action = QAction('Light Theme', self)
        two_theme_action = QAction('Dark Theme', self)
        three_theme_action = QAction('Blue Theme', self)
        four_theme_action = QAction('Green Theme', self)
        five_theme_action = QAction('Purple Theme', self)
        six_theme_action = QAction('Pink Theme', self)
        seven_theme_action = QAction('Yellow Theme', self)

        theme_menu.addAction(one_theme_action)
        theme_menu.addAction(two_theme_action)
        theme_menu.addAction(three_theme_action)
        theme_menu.addAction(four_theme_action)
        theme_menu.addAction(five_theme_action)
        theme_menu.addAction(six_theme_action)
        theme_menu.addAction(seven_theme_action)

        one_theme_action.triggered.connect(self.apply_one_theme)
        two_theme_action.triggered.connect(self.apply_two_theme)
        three_theme_action.triggered.connect(self.apply_three_theme)
        four_theme_action.triggered.connect(self.apply_four_theme)
        five_theme_action.triggered.connect(self.apply_five_theme)
        six_theme_action.triggered.connect(self.apply_six_theme)
        seven_theme_action.triggered.connect(self.apply_seven_theme)

        # 创建 'Help' 菜单
        help_menu = menubar.addMenu('Help')

        # 添加 Help 菜单项
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    # 显示关于对话框
    def show_about_dialog(self):
        QMessageBox.about(self, "关于", "这是一个 Maya 工具箱界面示例。")

    # 关闭窗口事件，保存窗口的大小和位置
    def closeEvent(self, event):
        self.write_settings()
        event.accept()

    # 读取窗口大小和位置的设置
    def read_settings(self):
        settings = QSettings("YourCompany", "SimpleMayaWindow")
        pos = settings.value("pos", QPoint(100, 100))
        size = settings.value("size", QSize(400, 400))
        self.move(pos)
        self.resize(size)

    # 写入窗口大小和位置的设置
    def write_settings(self):
        settings = QSettings("YourCompany", "SimpleMayaWindow")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def load_qss_from_file(self, file_path):
        try:
            # 使用 utf-8 编码读取文件
            with open(file_path, "r", encoding="utf-8") as file:
                qss = file.read()
                self.setStyleSheet(qss)  # 应用样式
        except FileNotFoundError:
            print(f"无法找到样式文件: {file_path}")
        except Exception as e:
            print(f"加载样式文件时发生错误: {str(e)}")

    def save_theme_setting(self, theme):
        settings = QSettings("YourCompany", "SimpleMayaWindow")
        settings.setValue("theme", theme)

    def apply_one_theme(self):
        # 使用硬编码的绝对路径
        qss_file = "F:/05 3D/syy_tool_set/QSS/one.qss"
        self.load_qss_from_file(qss_file)
        self.save_theme_setting("one")

    def apply_two_theme(self):
        qss_file = "F:/05 3D/syy_tool_set/QSS/two.qss"
        self.load_qss_from_file(qss_file)
        self.save_theme_setting("two")

    def apply_three_theme(self):
        qss_file = "F:/05 3D/syy_tool_set/QSS/three.qss"
        self.load_qss_from_file(qss_file)
        self.save_theme_setting("three")

    def apply_four_theme(self):
        qss_file = "F:/05 3D/syy_tool_set/QSS/four.qss"
        self.load_qss_from_file(qss_file)
        self.save_theme_setting("four")

    def apply_five_theme(self):
        qss_file = "F:/05 3D/syy_tool_set/QSS/five.qss"
        self.load_qss_from_file(qss_file)
        self.save_theme_setting("five")

    def apply_six_theme(self):
        qss_file = "F:/05 3D/syy_tool_set/QSS/six.qss"
        self.load_qss_from_file(qss_file)
        self.save_theme_setting("six")

    def apply_seven_theme(self):
        qss_file = "F:/05 3D/syy_tool_set/QSS/seven.qss"
        self.load_qss_from_file(qss_file)
        self.save_theme_setting("seven")

    def load_theme_setting(self):
        settings = QSettings("YourCompany", "SimpleMayaWindow")
        theme = settings.value("theme", "one")  # 默认是 'light' 主题

        if theme == "two":
            self.apply_two_theme()
        elif theme == "three":
            self.apply_three_theme()
        elif theme == "four":
            self.apply_four_theme()
        elif theme == "five":
            self.apply_five_theme()
        elif theme == "six":
            self.apply_six_theme()
        elif theme == "seven":
            self.apply_seven_theme()


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