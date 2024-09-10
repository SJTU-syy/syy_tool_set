import os
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFileDialog
from maya import cmds

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
