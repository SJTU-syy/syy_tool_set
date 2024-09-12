import sys

import maya.cmds as cmds
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

def get_maya_main_window():
    """
    获取 Maya 主窗口。
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QWidget)

def print_markdown_hierarchy():
    # 获取当前选择的对象
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        print("No objects selected.")
        return

    def print_hierarchy(obj, indent=0):
        # 输出对象及其子对象的目录结构
        print('  ' * indent + f'* {obj}')
        children = cmds.listRelatives(obj, children=True, type='transform') or []
        for child in children:
            print_hierarchy(child, indent + 1)

    for obj in selected_objects:
        print_hierarchy(obj)

def show_window_markdown_hierarchy():
    # 获取当前选择的对象
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        # 弹出提示框提醒用户没有选中对象
        QMessageBox.warning(None, "错误", "没有选中任何对象")
        return

    def generate_hierarchy(obj, indent=0):
        # 生成对象及其子对象的目录结构
        hierarchy = '  ' * indent + f'* {obj}\n'
        children = cmds.listRelatives(obj, children=True, type='transform') or []
        for child in children:
            hierarchy += generate_hierarchy(child, indent + 1)
        return hierarchy

    # 生成所有选中对象的 Markdown 结构
    markdown_structure = ""
    for obj in selected_objects:
        markdown_structure += generate_hierarchy(obj)

    # 获取 Maya 主窗口
    maya_main_window = get_maya_main_window()

    # 创建一个简单的 GUI 界面
    window = QWidget(maya_main_window)
    window.setWindowFlags(Qt.Window)  # 确保窗口是独立的
    window.setAttribute(Qt.WA_DeleteOnClose)  # 确保窗口关闭时被删除
    layout = QVBoxLayout(window)

    text_edit = QTextEdit()
    text_edit.setPlainText(markdown_structure)
    layout.addWidget(text_edit)

    def save_to_file():
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(window, "Save Markdown File", "", "Markdown Files (*.md);;All Files (*)", options=options)
        if file_name:
            if not file_name.endswith('.md'):
                file_name += '.md'
            with open(file_name, 'w') as file:
                file.write(markdown_structure)

    save_button = QPushButton("Save to .md File")
    save_button.clicked.connect(save_to_file)
    layout.addWidget(save_button)

    window.setLayout(layout)
    window.setWindowTitle("Markdown Hierarchy Viewer")
    window.show()

# 用于测试子窗口的打开方式，没什么必要，不如直接以maya为主界面打开
def show_test_window(parent=None):
    """
    显示测试窗口，使用指定的父窗口。
    """
    if parent and not isinstance(parent, QWidget):
        raise TypeError("The parent argument must be a QWidget instance or None.")

    # 创建窗口
    window = QWidget(parent)
    ###################这两条很重要很重要，通过函数打开界面就得这么写
    window.setWindowFlags(Qt.Window)  # 确保窗口是独立的
    window.setAttribute(Qt.WA_DeleteOnClose)  # 确保窗口关闭时被删除

    layout = QVBoxLayout(window)

    label = QLabel("Hello World!")
    label.setAlignment(Qt.AlignCenter)  # 标签居中对齐
    layout.addWidget(label)

    window.setLayout(layout)
    window.setWindowTitle("Test Window")
    window.resize(500, 500)  # 设置窗口大小
    window.show()


