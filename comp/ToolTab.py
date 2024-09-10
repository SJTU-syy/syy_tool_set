import os
from PySide2.QtWidgets import *
from maya import cmds

# Tool分页
class ToolTab(QWidget):
    def __init__(self, parent=None):
        super(ToolTab, self).__init__(parent)

        self.setWindowTitle("批量重命名")
        self.setGeometry(100, 100, 300, 200)

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建文本输入框
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("输入文本内容")
        main_layout.addWidget(self.text_input)

        # 创建前缀和后缀选择按钮
        self.prefix_radio = QRadioButton("前缀", self)
        self.suffix_radio = QRadioButton("后缀", self)
        self.prefix_radio.setChecked(True)

        # 创建按钮组
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.prefix_radio)
        self.button_group.addButton(self.suffix_radio)

        main_layout.addWidget(self.prefix_radio)
        main_layout.addWidget(self.suffix_radio)

        # 创建确定按钮
        self.ok_button = QPushButton("确定", self)
        self.ok_button.clicked.connect(self.rename_objects)
        main_layout.addWidget(self.ok_button)

        # 设置布局
        self.setLayout(main_layout)

    def rename_objects(self):
        text = self.text_input.text()
        if not text:
            QMessageBox.warning(self, "错误", "请输入文本内容")
            return

        # 获取选择的对象及其所有嵌套子对象
        selected_objects = cmds.ls(selection=True, dag=True, long=True)
        if not selected_objects:
            QMessageBox.warning(self, "错误", "请选择对象")
            return

        # 获取前缀或后缀选择
        is_prefix = self.prefix_radio.isChecked()

        # 批量重命名
        for obj in selected_objects:
            self.rename_recursive(obj, text, is_prefix)

        # 刷新界面并清空输入框
        self.refresh_ui()

        QMessageBox.information(self, "成功", "对象已重命名")

    def rename_recursive(self, obj, text, is_prefix):
        ''''''

        ''''''

        # 获取对象名称
        obj_name = cmds.ls(obj, long=False)[0]

        # 获取对象的所有子对象
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []

        # 过滤出骨骼节点
        joint_children = cmds.ls(children, type="joint")

        # 递归重命名子对象
        for child in joint_children:
            self.rename_recursive(child, text, is_prefix)

        # 重命名对象
        if is_prefix:
            new_name = f"{text}_{obj_name}"
        else:
            new_name = f"{obj_name}_{text}"
        cmds.rename(obj, new_name)

    def refresh_ui(self):
        # 清空输入框内容
        self.text_input.clear()

        # 重置前缀和后缀选择
        self.prefix_radio.setChecked(True)

        # 刷新界面
        self.update()

# 创建ToolTab实例
tool_tab = ToolTab()
tool_tab.show()
