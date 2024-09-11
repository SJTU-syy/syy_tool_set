from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QCheckBox
import maya.cmds as cmds
import time

# Setting分页
class SettingTab(QWidget):
    def __init__(self, parent=None):
        super(SettingTab, self).__init__(parent)
        layout = QVBoxLayout()

        # 添加功能说明标签
        layout.addWidget(QLabel("Setting功能说明"))

        # 添加Setting按钮1
        layout.addWidget(QPushButton("Setting按钮1"))

        # 添加Setting按钮2
        layout.addWidget(QPushButton("Setting按钮2"))

        # 添加自动保存时间间隔选择框
        self.auto_save_interval_label = QLabel("自动保存时间间隔 (分钟):")
        layout.addWidget(self.auto_save_interval_label)
        self.auto_save_interval_combo = QComboBox()
        self.auto_save_interval_combo.addItems(["5", "10", "15", "30", "60"])
        layout.addWidget(self.auto_save_interval_combo)

        # 添加默认工程名称文本框
        self.default_project_name_label = QLabel("默认工程名称:")
        layout.addWidget(self.default_project_name_label)
        self.default_project_name_edit = QLineEdit()
        layout.addWidget(self.default_project_name_edit)

        # 添加自动保存功能勾选框
        self.auto_save_checkbox = QCheckBox("开启自动保存功能")
        layout.addWidget(self.auto_save_checkbox)

        # 连接自动保存功能勾选框的信号
        self.auto_save_checkbox.stateChanged.connect(self.toggle_auto_save)

        self.setLayout(layout)

        # 初始化自动保存功能
        self.auto_save_timer = None
        self.toggle_auto_save(self.auto_save_checkbox.isChecked())

    def toggle_auto_save(self, state):
        """
        开启或关闭自动保存功能
        :param state: 勾选框的状态
        """
        if state:
            interval = int(self.auto_save_interval_combo.currentText()) * 60  # 转换为秒
            self.start_auto_save(interval)
        else:
            self.stop_auto_save()

    def start_auto_save(self, interval):
        """
        开始自动保存
        :param interval: 自动保存的时间间隔（秒）
        """
        if self.auto_save_timer is None:
            self.auto_save_timer = cmds.scriptJob(event=["idle", self.auto_save], runOnce=False)
        self.auto_save_interval = interval
        self.last_save_time = time.time()

    def stop_auto_save(self):
        """
        停止自动保存
        """
        if self.auto_save_timer is not None:
            cmds.scriptJob(kill=self.auto_save_timer)
            self.auto_save_timer = None

    def auto_save(self):
        """
        自动保存逻辑
        """
        current_time = time.time()
        if current_time - self.last_save_time >= self.auto_save_interval:
            project_name = self.default_project_name_edit.text()
            if project_name:
                cmds.file(rename=project_name)
            cmds.file(save=True, type="mayaAscii")
            self.last_save_time = current_time