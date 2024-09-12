import maya.cmds as cmds
from PySide2.QtWidgets import *
import sys


# 查找场景中的骨骼节点
def find_joint_nodes(joints, patterns):
    """
    查找场景中的骨骼节点，名称匹配指定模式的节点。

    :param joints: 要查找的骨骼节点列表
    :param patterns: 要匹配的模式列表，例如 ["Scapula", "Hip"]
    :return: 匹配的骨骼节点列表
    """
    # 用于存储匹配的节点
    matched_nodes = []

    for joint in joints:
        joint_name = joint.split('|')[-1]  # 去掉路径信息
        # 遍历模式列表
        for pattern in patterns:
            # print(f"正在匹配 {joint_name} 与 {pattern}")
            if joint_name in pattern:
                matched_nodes.append(joint)
                break  # 如果找到一个相同的名字，就跳出循环

    # 返回匹配的节点列表

    return matched_nodes

# 获取对象及其所有子对象的数组
def get_object_and_children(source_object):
    """
    获取对象及其所有子对象的数组

    :param source_object: 要获取的对象名称
    :return: 包含对象及其所有子对象的数组
    """
    # 获取对象及其所有子对象
    all_objects = cmds.listRelatives(source_object, allDescendents=True, fullPath=True) or []
    #尾部插入父对象
    all_objects.append(source_object)
    #翻转数组，使其从后往前遍历
    all_objects.reverse()

    return all_objects

# 判断两个关节是否有父子关系
def are_joints_parented(parent_joint, child_joint):
    """
    判断两个关节是否有父子关系

    :param parent_joint: 父关节的名称
    :param child_joint: 子关节的名称
    :return: 如果有父子关系返回 True，否则返回 False
    """
    # 获取子关节的父节点列表
    parents = cmds.listRelatives(child_joint, parent=True) or []

    # 检查父关节是否在子关节的父节点列表中
    return parent_joint in parents


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
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()

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
    sys.exit(app.exec_())
