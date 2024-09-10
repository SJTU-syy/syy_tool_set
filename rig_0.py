import os
import sys
from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

# 获取Maya主窗口的指针
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QMainWindow)

# 创建一个主窗口类
class SimpleMayaWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SimpleMayaWindow, self).__init__(parent)
        self.setWindowTitle("加载.ma文件")
        self.setGeometry(100, 100, 400, 200)

        # 创建一个主布局
        main_layout = QVBoxLayout()

        # 创建一个标签
        self.label = QLabel("选择一个.ma文件", self)
        main_layout.addWidget(self.label)

        # 创建一个下拉框
        self.combo_box = QComboBox(self)
        self.populate_combo_box()
        main_layout.addWidget(self.combo_box)

        # 创建一个按钮
        self.button = QPushButton("导入", self)
        self.button.clicked.connect(self.load_file)
        main_layout.addWidget(self.button)

        # 创建一个中心部件并设置布局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # 填充下拉框
    def populate_combo_box(self):
        directory = r"F:\MAYA\proj\AdvancedSkeleton\AdvancedSkeletonFiles\fitSkeletons"
        if os.path.exists(directory):
            for file_name in os.listdir(directory):
                if file_name.endswith(".ma"):
                    self.combo_box.addItem(file_name)
        else:
            self.combo_box.addItem("目录不存在")

    # 加载选中的文件
    def load_file(self):
        selected_file = self.combo_box.currentText()
        if selected_file != "目录不存在":
            file_path = os.path.join(r"F:\MAYA\proj\AdvancedSkeleton\AdvancedSkeletonFiles\fitSkeletons", selected_file)
            cmds.file(file_path, i=True, force=True)
            QMessageBox.information(self, "成功", f"文件 {selected_file} 已加载到当前场景中")
        else:
            QMessageBox.warning(self, "错误", "目录不存在")

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
