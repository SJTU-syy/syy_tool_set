import os
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QCheckBox, QMessageBox, QFileDialog, QGroupBox, QFormLayout
import maya.cmds as cmds
import time

# Setting分页
class SettingTool(QWidget):
    def __init__(self, parent=None):
        super(SettingTool, self).__init__(parent)
        main_layout = QVBoxLayout()

        # 骨骼模板部分
        import_group = QGroupBox("骨骼模板管理")
        import_layout = QVBoxLayout()

        # 导入骨骼模板
        self.label = QLabel("选择一个 .ma 文件", self)
        import_layout.addWidget(self.label)

        self.combo_box = QComboBox(self)
        self.populate_combo_box()
        import_layout.addWidget(self.combo_box)

        self.import_button = QPushButton("导入", self)
        self.import_button.clicked.connect(self.load_file)
        import_layout.addWidget(self.import_button)

        # 导出骨骼模板
        self.export_button = QPushButton("导出骨骼模板", self)
        self.export_button.clicked.connect(self.export_file)
        import_layout.addWidget(self.export_button)

        import_group.setLayout(import_layout)
        main_layout.addWidget(import_group)

        # 自动保存部分
        autosave_group = QGroupBox("自动保存设置")
        autosave_layout = QFormLayout()

        self.auto_save_interval_label = QLabel("自动保存时间间隔 (分钟):")
        self.auto_save_interval_combo = QComboBox()
        self.auto_save_interval_combo.addItems(["5", "10", "15", "30", "60"])
        autosave_layout.addRow(self.auto_save_interval_label, self.auto_save_interval_combo)

        self.default_project_name_label = QLabel("自动保存工程名称:")
        self.default_project_name_edit = QLineEdit()
        autosave_layout.addRow(self.default_project_name_label, self.default_project_name_edit)

        self.auto_save_checkbox = QCheckBox("开启自动保存功能")
        self.auto_save_checkbox.stateChanged.connect(self.toggle_auto_save)
        autosave_layout.addRow(self.auto_save_checkbox)

        autosave_group.setLayout(autosave_layout)
        main_layout.addWidget(autosave_group)

        # 添加与Project工具相关的功能
        project_group = QGroupBox("Project 工具")
        project_layout = QVBoxLayout()

        self.project_label = QLabel("设置工程目录", self)
        project_layout.addWidget(self.project_label)

        self.project_directory_edit = QLineEdit(self)
        self.project_directory_edit.setPlaceholderText("选择或输入项目目录...")
        project_layout.addWidget(self.project_directory_edit)

        self.select_project_button = QPushButton("选择项目目录", self)
        self.select_project_button.clicked.connect(self.select_project_directory)
        project_layout.addWidget(self.select_project_button)

        self.create_standard_folders_button = QPushButton("创建标准文件夹", self)
        self.create_standard_folders_button.clicked.connect(self.create_standard_folders)
        project_layout.addWidget(self.create_standard_folders_button)

        project_group.setLayout(project_layout)
        main_layout.addWidget(project_group)

        # 设置主布局
        self.setLayout(main_layout)

        # 初始化自动保存功能
        self.auto_save_timer = None
        self.toggle_auto_save(self.auto_save_checkbox.isChecked())

    def populate_combo_box(self):
        """填充ComboBox"""
        directory = os.path.abspath(__file__ + "/../ma")
        if os.path.exists(directory):
            for file_name in os.listdir(directory):
                if file_name.endswith(".ma"):
                    self.combo_box.addItem(file_name)
        else:
            self.combo_box.addItem("目录不存在")

    def load_file(self):
        """导入选中的文件"""
        selected_file = self.combo_box.currentText()
        if selected_file != "目录不存在":
            file_path = os.path.abspath(__file__ + "/../ma/" + selected_file)

            # 检查场景中是否已经存在名为FitSkeleton的transform
            if cmds.objExists("FitSkeleton"):
                reply = QMessageBox.question(self, "提示", "场景中已导入过骨骼模板，是否重新导入？",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cmds.delete("FitSkeleton")
                else:
                    return

            cmds.file(file_path, i=True, force=True)
            QMessageBox.information(self, "成功", f"文件 {selected_file} 已加载到当前场景中")
        else:
            QMessageBox.warning(self, "错误", "目录不存在")

    def export_file(self):
        """导出当前场景"""
        file_path, _ = QFileDialog.getSaveFileName(self, "导出当前场景", "", "Maya ASCII (*.ma)")
        if file_path:
            cmds.file(rename=file_path)
            cmds.file(save=True, type="mayaAscii")
            QMessageBox.information(self, "成功", f"当前场景已导出为 {file_path}")

    def toggle_auto_save(self, state):
        """开启或关闭自动保存功能"""
        if state:
            interval = int(self.auto_save_interval_combo.currentText()) * 60  # 转换为秒
            self.start_auto_save(interval)
        else:
            self.stop_auto_save()

    def start_auto_save(self, interval):
        """开始自动保存"""
        if self.auto_save_timer is None:
            self.auto_save_timer = cmds.scriptJob(event=["idle", self.auto_save], runOnce=False)
        self.auto_save_interval = interval
        self.last_save_time = time.time()

    def stop_auto_save(self):
        """停止自动保存"""
        if self.auto_save_timer is not None:
            cmds.scriptJob(kill=self.auto_save_timer)
            self.auto_save_timer = None

    def auto_save(self):
        """自动保存逻辑"""
        current_time = time.time()
        if current_time - self.last_save_time >= self.auto_save_interval:
            project_name = self.default_project_name_edit.text()
            if project_name:
                cmds.file(rename=project_name)
            cmds.file(save=True, type="mayaAscii")
            self.last_save_time = current_time

    # 新功能：选择工程目录
    def select_project_directory(self):
        """选择Maya工程目录"""
        project_directory = QFileDialog.getExistingDirectory(self, "选择项目目录")
        if project_directory:
            self.project_directory_edit.setText(project_directory)
            cmds.workspace(project_directory, openWorkspace=True)
            QMessageBox.information(self, "成功", f"已设置工程目录: {project_directory}")

    # 新功能：创建标准文件夹
    def create_standard_folders(self):
        """创建标准的工程文件夹结构"""
        project_directory = self.project_directory_edit.text()
        if project_directory and os.path.exists(project_directory):
            # 定义标准文件夹列表
            standard_folders = ["scenes", "images", "sourceimages", "assets", "cache", "clips"]
            for folder in standard_folders:
                folder_path = os.path.join(project_directory, folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
            QMessageBox.information(self, "成功", f"已创建标准文件夹在 {project_directory}")
        else:
            QMessageBox.warning(self, "错误", "无效的项目目录")



def main():
    return SettingTool()

if __name__ == '__main__':
    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = SettingTool ()  # 创建实例
    window.show ()  # 显示窗口