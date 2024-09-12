import maya.cmds as cmds
from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance





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
        print("No objects selected.")
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

    # 创建一个简单的 GUI 界面
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QWidget)

    window = QWidget(maya_main_window)
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
