import os
from PySide2.QtWidgets import *
from maya import cmds


import comp
import func
from rig import *
reload_modules('comp')
reload_modules('func')

# Tool分页
class NameTab(QWidget):
    def __init__(self, parent=None):
        super(NameTab, self).__init__(parent)

        self.setWindowTitle("重命名")
        self.setGeometry(100, 100, 400, 300)  # 增加窗口大小

        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)  # 设置控件间距
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置布局边距

        # 重命名任意对象
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("输入文本内容")
        main_layout.addWidget(self.text_input)

        self.prefix_radio = QRadioButton("前缀", self)
        self.suffix_radio = QRadioButton("后缀", self)
        self.prefix_radio.setChecked(True)

        self.hierarchy_radio = QRadioButton("继承", self)
        self.single_radio = QRadioButton("不继承", self)
        self.hierarchy_radio.setChecked(True)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.prefix_radio)
        self.button_group.addButton(self.suffix_radio)

        main_layout.addWidget(self.prefix_radio)
        main_layout.addWidget(self.suffix_radio)
        main_layout.addWidget(self.hierarchy_radio)
        main_layout.addWidget(self.single_radio)

        self.ok_button = QPushButton("确定", self)
        self.ok_button.clicked.connect(self.tab_rename_recursive)
        main_layout.addWidget(self.ok_button)

        # 打印目录结构
        self.print_button = QPushButton("打印目录结构", self)
        self.print_button.clicked.connect(func.FuncUtil.print_markdown_hierarchy)
        main_layout.addWidget(self.print_button)

        # 保存目录结构
        self.save_structure_button = QPushButton("保存结构", self)
        self.save_structure_button.clicked.connect(self.tab_show_markdown_hierarchy)
        main_layout.addWidget(self.save_structure_button)

        # 弹出测试弹窗
        self.test_button = QPushButton("测试弹窗", self)
        self.test_button.clicked.connect(self.tab_show_test_window)
        main_layout.addWidget(self.test_button)

        # 设置布局
        self.setLayout(main_layout)
        # 应用QSS样式
        self.setStyleSheet("""
                    QWidget {
                        background-color: #2E2E2E;  /* 背景颜色 */
                        color: #FFFFFF;  /* 字体颜色 */
                        font-family: Arial;
                    }
                    QLineEdit {
                        background-color: #444444;
                        color: #FFFFFF;
                        border: 1px solid #888888;
                        padding: 5px;
                        border-radius: 3px;  /* 圆角 */
                    }
                    QRadioButton {
                        color: #FFFFFF;
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #007ACC;  /* 按钮背景颜色 */
                        color: #FFFFFF;  /* 按钮字体颜色 */
                        border: none;
                        border-radius: 5px;  /* 圆角 */
                        padding: 10px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #005F99;  /* 鼠标悬停颜色 */
                    }
                    QPushButton:pressed {
                        background-color: #003F66;  /* 鼠标按下颜色 */
                    }
                """)

    def tab_rename_recursive(self):
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

        # 获取继承还是不继承选择
        is_hierarchy = self.hierarchy_radio.isChecked()

        # 批量重命名
        for obj in selected_objects:
            func.FuncName.rename_recursive(obj, text, is_prefix, is_hierarchy)

        # 刷新界面并清空输入框
        self.refresh_ui()

        QMessageBox.information(self, "成功", "对象已重命名")

    def tab_show_test_window(self):
        func.FuncUtil.show_test_window(self)

    def tab_show_markdown_hierarchy(self):
        func.FuncUtil.show_window_markdown_hierarchy(self)

    def refresh_ui(self):
        # 清空输入框内容
        self.text_input.clear()

        # 重置前缀和后缀选择
        self.prefix_radio.setChecked(True)

        # 刷新界面
        self.update()
