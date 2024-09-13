from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFileDialog
from maya import cmds

import comp
import func
from rig import *
reload_modules('comp')
reload_modules('func')

# 设置存放.ma文件的目录
Fpath = r"F:\Pycharm2024\pythonProject\AdvancedSkeleton\AdvancedSkeletonFiles\fitSkeletons"
#F:\Pycharm2024\pythonProject\AdvancedSkeleton\AdvancedSkeletonFiles\fitSkeletons

class BodyTab(QWidget):
    def __init__(self, parent=None):
        super(BodyTab, self).__init__(parent)

        self._temp_model = None

        # 创建一个主布局
        main_layout = QVBoxLayout()


        # 导入骨骼模板
        self.label = QLabel("选择一个.ma文件", self)
        main_layout.addWidget(self.label)

        self.combo_box = QComboBox(self)
        self.populate_combo_box()
        main_layout.addWidget(self.combo_box)

        self.button = QPushButton("导入", self)
        self.button.clicked.connect(self.load_file)
        main_layout.addWidget(self.button)

        # 导出骨骼模板
        self.export_button = QPushButton("导出", self)
        self.export_button.clicked.connect(self.export_file)
        main_layout.addWidget(self.export_button)

        # 创建对称骨骼
        self.create_symmetric_skeleton_button = QPushButton("创建对称骨骼系统", self)
        self.create_symmetric_skeleton_button.clicked.connect(self.create_symmetric_skeleton)
        main_layout.addWidget(self.create_symmetric_skeleton_button)

        # 添加所有控制器
        self.add_all_controllers_button = QPushButton("添加所有控制器", self)
        self.add_all_controllers_button.clicked.connect(self.add_all_controllers)
        main_layout.addWidget(self.add_all_controllers_button)

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

    # 导入选中的文件
    def load_file(self):
        selected_file = self.combo_box.currentText()
        if selected_file != "目录不存在":
            file_path = os.path.join(Fpath, selected_file)

            # 检查场景中是否已经存在名为FitSkeleton的transform
            if cmds.objExists("FitSkeleton"):
                reply = QMessageBox.question(self, "提示", "场景中已导入过骨骼模板，是否重新导入？",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # 删除旧的FitSkeleton
                    cmds.delete("FitSkeleton")
                else:
                    return

            # 加载新模板
            cmds.file(file_path, i=True, force=True)
            self._temp_model = selected_file
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

    # 创建之前导入的ma骨骼编辑后的对称骨骼系统
    def create_symmetric_skeleton(self):
        print("创建对称骨骼系统")

        # 寻找场景中的 FitSkeleton 对象
        fit_skeleton = cmds.ls("FitSkeleton", type="transform")
        if not fit_skeleton:
            cmds.error("FitSkeleton 对象未找到")
            return

        fit_skeleton = fit_skeleton[0]
        # 复制 FitSkeleton
        fit_skeleton_copy = cmds.duplicate(fit_skeleton, name="FitSkeleton_copy")[0]

        # # 查询连接的节点
        # connections = cmds.listConnections(fit_skeleton + ".v", plugs=True, connections=True)
        # if connections:
        #     # 断开连接
        #     cmds.disconnectAttr(connections[0], connections[1])
        # #将原来的fit_skeleton设定为隐藏
        # cmds.setAttr(fit_skeleton + ".v", 0)

        #将原来的fit_skeleton删除 @TODO: 待优化
        cmds.delete(fit_skeleton)


        # 获取 FitSkeleton_copy 的子对象
        children = cmds.listRelatives(fit_skeleton_copy, children=True, fullPath=True) or []
        # 获取所有骨骼节点
        all_joints = cmds.listRelatives(fit_skeleton_copy, allDescendents=True, type="joint", fullPath=True) or []

        # @TODO: 根据不同的骨骼类型添加更多需要镜像的节点
        patterns = ["Scapula", "Hip"]
        matched_nodes = func.FuncNode.find_joint_nodes(all_joints, patterns)
        print(f"匹配的骨骼节点：{matched_nodes}")

        for joint in matched_nodes:
            func.FuncRig.create_mirrored_joint(joint)


    # 添加所有控制器
    def add_all_controllers(self):
        if self._temp_model is None:
            QMessageBox.warning(self, "错误", "请先导入模型")
            return

        # 根据不同的模型名称，为不同的骨骼添加控制器
        if self._temp_model == 'biped.ma':
            func.FuncControl.add_biped_controllers(self)
        else:
            QMessageBox.warning(self, "提示", "当前模型没有预定义的控制器")


