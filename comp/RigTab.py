from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QLineEdit

# RigTab 类
class RigTab(QWidget):
    def __init__(self, parent=None):
        super(RigTab, self).__init__(parent)

        # 总布局
        layout = QVBoxLayout()

        # 功能说明标签
        layout.addWidget(QLabel("Facial功能说明"))

        # 默认连接部分
        layout.addWidget(QLabel("连接默认属性"))

        # 属性复选框
        self.translate_checkbox = QCheckBox("Translate")
        self.rotate_checkbox = QCheckBox("Rotate")
        self.scale_checkbox = QCheckBox("Scale")
        self.matrix_checkbox = QCheckBox("Matrix")

        # 添加复选框到布局
        attr_layout = QHBoxLayout()
        attr_layout.addWidget(self.translate_checkbox)
        attr_layout.addWidget(self.rotate_checkbox)
        attr_layout.addWidget(self.scale_checkbox)
        attr_layout.addWidget(self.matrix_checkbox)

        layout.addLayout(attr_layout)

        # 创建和删除连接按钮
        self.create_default_btn = QPushButton("创建连接")
        self.delete_default_btn = QPushButton("删除连接")

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_default_btn)
        button_layout.addWidget(self.delete_default_btn)

        layout.addLayout(button_layout)

        # 自定义连接部分
        layout.addWidget(QLabel("连接自定义属性"))

        # 自定义连接输入框
        self.driver_input = QLineEdit()
        self.driver_input.setPlaceholderText("Driver (驱动者)")
        self.driven_input = QLineEdit()
        self.driven_input.setPlaceholderText("Driven (被驱动者)")

        # 添加输入框到布局
        custom_attr_layout = QVBoxLayout()
        custom_attr_layout.addWidget(self.driver_input)
        custom_attr_layout.addWidget(self.driven_input)

        layout.addLayout(custom_attr_layout)

        # 自定义连接按钮
        self.create_custom_btn = QPushButton("创建自定义连接")
        self.delete_custom_btn = QPushButton("删除自定义连接")

        # 添加自定义连接按钮到布局
        custom_button_layout = QHBoxLayout()
        custom_button_layout.addWidget(self.create_custom_btn)
        custom_button_layout.addWidget(self.delete_custom_btn)

        layout.addLayout(custom_button_layout)

        # 设置布局
        self.setLayout(layout)

        # 连接信号与槽
        self.create_default_btn.clicked.connect(self.create_default_connection)
        self.delete_default_btn.clicked.connect(self.delete_default_connection)
        self.create_custom_btn.clicked.connect(self.create_custom_connection)
        self.delete_custom_btn.clicked.connect(self.delete_custom_connection)

    def create_default_connection(self):
        # 根据复选框选择的属性创建连接的逻辑
        pass

    def delete_default_connection(self):
        # 删除默认连接的逻辑
        pass

    def create_custom_connection(self):
        # 基于输入框的内容创建自定义连接
        driver = self.driver_input.text()
        driven = self.driven_input.text()
        if driver and driven:
            print(f"创建连接: {driver} -> {driven}")
            # 使用 Maya 命令创建连接
            pass

    def delete_custom_connection(self):
        # 删除自定义连接的逻辑
        pass