from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QFileDialog, \
    QSpinBox
from PySide2.QtCore import Qt, Slot
import maya.cmds as cmds


import comp
import func
from rig import *
reload_modules('comp')
reload_modules('func')

class AnimTab(QWidget):
    def __init__(self):
        super(AnimTab, self).__init__()

        # 初始化布局
        self.layout = QVBoxLayout()

        # 关键帧操作布局
        self.init_keyframe_controls()

        # 曲线操作布局
        self.init_curve_controls()

        # 动画操作布局
        self.init_animation_controls()

        # 设置主布局
        self.setLayout(self.layout)

    def init_keyframe_controls(self):
        # 关键帧操作
        keyframe_layout = QVBoxLayout()
        keyframe_layout.addWidget(QLabel("关键帧操作"))

        # 自动插入关键帧
        self.auto_start_frame = QSpinBox()
        self.auto_start_frame.setRange(0, 10000)
        self.auto_start_frame.setPrefix("开始帧: ")

        self.auto_end_frame = QSpinBox()
        self.auto_end_frame.setRange(0, 10000)
        self.auto_end_frame.setPrefix("结束帧: ")

        self.auto_interval = QSpinBox()
        self.auto_interval.setRange(1, 1000)
        self.auto_interval.setPrefix("间隔帧: ")

        auto_key_button = QPushButton("自动插入关键帧")
        auto_key_button.clicked.connect(self.auto_keyframe)

        keyframe_layout.addWidget(self.auto_start_frame)
        keyframe_layout.addWidget(self.auto_end_frame)
        keyframe_layout.addWidget(self.auto_interval)
        keyframe_layout.addWidget(auto_key_button)

        # 重置关键帧
        reset_key_button = QPushButton("重置关键帧")
        reset_key_button.clicked.connect(self.reset_keyframes)

        keyframe_layout.addWidget(reset_key_button)

        # 导出关键帧
        export_key_button = QPushButton("导出关键帧")
        export_key_button.clicked.connect(self.export_keyframes)

        keyframe_layout.addWidget(export_key_button)

        self.layout.addLayout(keyframe_layout)

    def init_curve_controls(self):
        # 曲线操作
        curve_layout = QVBoxLayout()
        curve_layout.addWidget(QLabel("曲线操作"))

        # 创建自定义曲线
        curve_name_input = QLineEdit()
        curve_name_input.setPlaceholderText("曲线名称")

        create_curve_button = QPushButton("创建自定义曲线")
        create_curve_button.clicked.connect(self.create_custom_curve)

        curve_layout.addWidget(curve_name_input)
        curve_layout.addWidget(create_curve_button)

        self.layout.addLayout(curve_layout)

    def init_animation_controls(self):
        # 动画操作
        animation_layout = QVBoxLayout()
        animation_layout.addWidget(QLabel("动画操作"))

        # 镜像动画
        self.source_joint_input = QLineEdit()
        self.source_joint_input.setPlaceholderText("源关节")

        self.target_joint_input = QLineEdit()
        self.target_joint_input.setPlaceholderText("目标关节")

        mirror_button = QPushButton("镜像动画")
        mirror_button.clicked.connect(self.mirror_animation)

        animation_layout.addWidget(self.source_joint_input)
        animation_layout.addWidget(self.target_joint_input)
        animation_layout.addWidget(mirror_button)

        self.layout.addLayout(animation_layout)

    ############################################################
    # 关键帧操作的槽函数
    ############################################################
    @Slot()
    def auto_keyframe(self):
        start_frame = self.auto_start_frame.value()
        end_frame = self.auto_end_frame.value()
        interval = self.auto_interval.value()
        attributes = ['translateX', 'translateY', 'translateZ']  # 你可以在这里扩展需要自动插入的属性
        func.FuncAnim.auto_keyframe_insertion(start_frame, end_frame, interval, attributes)

    @Slot()
    def reset_keyframes(self):
        objects = cmds.ls(selection=True)
        start_frame = 0  # 这里可以自定义时间范围
        end_frame = 100
        func.FuncAnim.reset_keyframes(objects, start_frame, end_frame)

    @Slot()
    def export_keyframes(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "导出关键帧", "", "Text Files (*.txt)")
        if file_path:
            func.FuncAnim.export_keyframes(file_path)

    ############################################################
    # 曲线操作的槽函数
    ############################################################
    @Slot()
    def create_custom_curve(self):
        curve_name = self.sender().parentWidget().findChild(QLineEdit).text()
        keyframes = [1, 10, 20]  # 自定义的关键帧
        values = [0, 5, 10]  # 对应关键帧的值
        func.FuncAnim.create_custom_curve(curve_name, keyframes, values)

    ############################################################
    # 动画操作的槽函数
    ############################################################
    @Slot()
    def mirror_animation(self):
        source_joint = self.source_joint_input.text()
        target_joint = self.target_joint_input.text()
        start_frame = 1  # 动画开始帧
        end_frame = 100  # 动画结束帧
        func.FuncAnim.mirror_animation(source_joint, target_joint, start_frame, end_frame)
