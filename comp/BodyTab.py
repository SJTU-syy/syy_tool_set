import os
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFileDialog
from maya import cmds

# 设置存放文件路径
Fpath = r"F:\MAYA\proj\AdvancedSkeleton\AdvancedSkeletonFiles\fitSkeletons"

class BodyTab(QWidget):
    def __init__(self, parent=None):
        super(BodyTab, self).__init__(parent)

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

        # 创建一个导出按钮
        self.export_button = QPushButton("导出", self)
        self.export_button.clicked.connect(self.export_file)
        main_layout.addWidget(self.export_button)

        # 创建一个创建对称骨骼系统的按钮
        self.create_symmetric_skeleton_button = QPushButton("创建对称骨骼系统", self)
        self.create_symmetric_skeleton_button.clicked.connect(self.create_symmetric_skeleton)
        main_layout.addWidget(self.create_symmetric_skeleton_button)

        # 设置布局
        self.setLayout(main_layout)

    # 填充下拉框
    def populate_combo_box(self):
        directory = Fpath
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
            file_path = os.path.join(Fpath, selected_file)

            # 检查场景中是否已经存在名为FitSkeleton的transform
            if cmds.objExists("FitSkeleton"):
                reply = QMessageBox.question(self, "提示", "场景中已经存在名为FitSkeleton的transform，是否继续导入？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return

            cmds.file(file_path, i=True, force=True)
            QMessageBox.information(self, "成功", f"文件 {selected_file} 已加载到当前场景中")
        else:
            QMessageBox.warning(self, "错误", "目录不存在")

    # 导出当前场景
    def export_file(self):
        # 打开文件对话框，选择导出路径
        file_path, _ = QFileDialog.getSaveFileName(self, "导出当前场景", "", "Maya ASCII (*.ma)")
        if file_path:
            cmds.file(rename=file_path)
            cmds.file(save=True, type="mayaAscii")
            QMessageBox.information(self, "成功", f"当前场景已导出为 {file_path}")

    # 创建对称骨骼系统
    def create_symmetric_skeleton(self):

        # 寻找场景中的 FitSkeleton 对象
        fit_skeleton = cmds.ls("FitSkeleton", type="transform")
        if not fit_skeleton:
            cmds.error("FitSkeleton 对象未找到")
            return

        fit_skeleton = fit_skeleton[0]
        # 复制 FitSkeleton
        fit_skeleton_copy = cmds.duplicate(fit_skeleton, name="FitSkeleton_copy")[0]


        # 获取 FitSkeleton_copy 的子对象
        children = cmds.listRelatives(fit_skeleton_copy, children=True, fullPath=True) or []
        # 获取所有骨骼节点
        all_joints = cmds.listRelatives(fit_skeleton_copy, allDescendents=True, type="joint", fullPath=True) or []

        # 过滤出名字包含 "Scapula" 和 "Hip" 的骨骼节点
        patterns = ["Scapula", "Hip"]
        matched_nodes = self.find_joint_nodes(all_joints, patterns)

        # 生成对称骨骼结构
        symmetric_nodes = []
        for node in matched_nodes:
            # 获取节点名称
            node_name = cmds.ls(node, long=False)[0]
            print(f"正在生成对称骨骼 {node_name}")


            # 创建对称节点
            symmetric_node = cmds.duplicate(node, name=f"{node_name.split('|')[-1]}_symmetric")[0]

            symmetric_nodes.append(symmetric_node)

            # 获取节点的世界坐标位置
            position = cmds.xform(node, query=True, translation=True, worldSpace=True)

            # 生成对称位置并设置到对称节点上
            symmetric_position = [-position[0], position[1], position[2]]
            cmds.xform(symmetric_node, translation=symmetric_position, worldSpace=True)

            cmds.setAttr(f"{node}.rotateOrder", 0)
            cmds.setAttr(f"{symmetric_node}.rotateOrder", 0)
            # 将对称节点的旋转设置为原节点的对称旋转
            rotation = cmds.xform(node, query=True, rotation=True, worldSpace=True)
            print(f"原节点的旋转为 {rotation}")
            # 对于左右对称，X轴旋转是反向的，而Y和Z轴旋转不变
            symmetric_rotation = [-rotation[0], rotation[1], rotation[2]]
            print(f"对称节点的旋转为 {symmetric_rotation}")
            cmds.xform(symmetric_node, rotation=symmetric_rotation, worldSpace=True)

            # # 将对称节点的父节点设为原节点的父节点
            # parent = cmds.listRelatives(node, parent=True, fullPath=True)
            # if parent:
            #     cmds.parent(symmetric_node, parent)

        # # 创建一个名为 DeformationSystem 的空组
        # deformation_system = cmds.group(empty=True, name="DeformationSystem")
        # # 将新的对称骨骼系统添加到 DeformationSystem 组中
        # cmds.parent(fit_skeleton_copy, deformation_system)
        #
        # # 创建一个名为 Advanced 的组
        # advanced_group = cmds.group(empty=True, name="Advanced")
        # # 将 DeformationSystem 和原来的 FitSkeleton 合并到 Advanced 组中
        # cmds.parent([deformation_system, fit_skeleton], advanced_group)

        # print("对称骨骼系统已创建并添加到 Advanced 组中")

    # 查找场景中的骨骼节点
    def find_joint_nodes(self, joints, patterns):
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
