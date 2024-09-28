import sys
from importlib import reload

import maya.cmds as cmds
import pymel.core as pm
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .config import icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils , qtUtils , controlUtils , snapUtils , attrUtils , fileUtils , \
    hierarchyUtils , weightsUtils
from . import skirt_ctrl_tool

reload (qtUtils)
reload (controlUtils)
reload (attrUtils)
reload (fileUtils)
reload (jointUtils)
reload(skirt_ctrl_tool)

class Rig_Tool (QWidget) :
    """
    一个绑定工具的类
    """


    def __init__ (self , parent = None) :
        super (Rig_Tool , self).__init__ (parent)
        self.win_name = 'Rig_Tool'
        self.win_title = 'Rig_Tool(绑定工具)'
        self.create_widgets ()
        self.create_layouts ()
        self.add_connnect ()


    def create_widgets (self) :
        # FK
        self.fk_label = QLabel ('---------------创建FK系统----------------')
        self.fk_label.setStyleSheet (u"color: rgb(85, 255, 255);")
        self.create_fk_button = QPushButton (QIcon (':kinConnect.png') , '创建fk系统')
        self.delete_fk_button = QPushButton (QIcon (':kinConnect.png') , '删除fk系统')
        # 添加文字提示
        self.create_fk_button.setToolTip ('将选择的物体创建fk绑定系统')
        self.delete_fk_button.setToolTip ('将选择的物体删除fk绑定系统')

        # IK
        self.ik_label = QLabel ('---------------创建IK系统----------------')
        self.ik_label.setStyleSheet (u"color: rgb(169, 255, 175);")
        self.ik_start_button = QPushButton (QIcon (':kinJoint.png') , '拾取IK链条起始关节')
        self.ik_start_button.setToolTip ('拾取ik起始关节')
        self.ik_start_line = QLineEdit ()
        self.ik_end_button = QPushButton (QIcon (':kinJoint.png') , '拾取IK链条结束关节')
        self.ik_end_button.setToolTip ('拾取ik结束关节')
        self.ik_end_line = QLineEdit ()
        self.create_ik_button = QPushButton (QIcon (':kinConnect.png') , '创建ik系统')
        self.delete_ik_button = QPushButton (QIcon (':kinConnect.png') , '删除ik系统')

        # 添加文字提示
        self.create_ik_button.setToolTip ('将选择的物体创建ik绑定系统')
        self.delete_ik_button.setToolTip ('将选择的物体删除ik绑定系统')

        # 工具
        self.tool_label = QLabel ('---------------绑定小工具---------------')
        self.tool_label.setStyleSheet (u"color: rgb(170, 255, 128);")
        self.create_tool_widgets ()


    def create_tool_widgets (self) :
        self.clear_keys_button = QPushButton (QIcon (icon_dir + '/key .png') , "删除关键帧")

        self.reset_attr_button = QPushButton (QIcon (icon_dir + '/icon-resetting.png') , "重置属性")

        self.batch_Constraints_modle_button = QPushButton (QIcon (':parentConstraint.png') , "批量约束_物体")

        self.batch_Constraints_joint_button = QPushButton (QIcon (':parentConstraint.png') , "批量约束_关节")

        self.default_grp_button = QPushButton (QIcon (icon_dir + '/hierarchy-fill.png') , "绑定层级组")

        self.control_hierarchy_button = QPushButton (QIcon (icon_dir + '/hierarchy-fill.png') , "自动打组(自用)")

        self.save_skinWeights_button = QPushButton (QIcon (':exportSmoothSkin.png') , u"导出权重")

        self.load_skinWeights_button = QPushButton (QIcon (':importSmoothSkin.png') , u"导入权重")

        self.select_sub_objects_button = QPushButton (QIcon (icon_dir + '/hierarchy-fill.png') , "快速选择子物体")

        self.print_duplicate_object_button = QPushButton (QIcon (icon_dir + '/RENAME.png') , "检查并列出重名节点")

        self.rename_duplicate_object_button = QPushButton (QIcon (icon_dir + '/rename (1).png') ,
                                                           "检查并重命名重名节点")

        self.create_dynamic_curve_driven_button = QPushButton (QIcon (':hairDynamicCurves.png') ,
                                                               "创建动力学化曲线驱动头发")
        self.snap_modle_button = QPushButton (QIcon (':menuIconModify.png') ,
                                              "吸附物体")

        self.export_animation_button = QPushButton (QIcon (':setKeyframe.png') ,
                                                    "导出选择的动画")
        self.import_animation_button = QPushButton (QIcon (':setKeyOnAnim.png') ,
                                                    "导入选择的动画")

        self.create_secondary_joint_button = QPushButton (QIcon (':parentConstraint.png') , "批量约束_次级")
        self.import_test_animation_button = QPushButton (QIcon (':setKeyOnAnim.png') ,
                                                         "导入动作测试的动画")

        self.skirt_ctrl_tool_btn = QPushButton('裙子控制器工具')
        # 添加文本提示
        self.clear_keys_button.setToolTip ('将场景内所有的动画关键帧删除')

        self.reset_attr_button.setToolTip ('重置选择的物体的属性')

        self.batch_Constraints_modle_button.setToolTip ('批量约束所选择的物体')
        self.batch_Constraints_joint_button.setToolTip ('批量约束所选择的关节')

        self.default_grp_button.setToolTip ('创建默认的绑定层级组')

        self.control_hierarchy_button.setToolTip ('自动将符合名称规范的控制器打组,ctrl_(side)_(description)_(index)')

        self.save_skinWeights_button.setToolTip ('将选择的物体的蒙皮权重导出到文件路径旁')

        self.load_skinWeights_button.setToolTip ('将选择的物体的蒙皮权重导入')

        self.select_sub_objects_button.setToolTip ('快速选择所选择物体的子物体')

        self.print_duplicate_object_button.setToolTip ('检查并列出场景里具有的重名节点')

        self.rename_duplicate_object_button.setToolTip ('检查并重命名场景里的重名节点')

        self.create_dynamic_curve_driven_button.setToolTip ('选择曲线，创建动力学曲线驱动')
        self.snap_modle_button.setToolTip ('选择物体，将最后的物体吸附到前面物体的中心')

        self.export_animation_button.setToolTip ('选择控制器导出到动画到对应的json文件里')
        self.import_animation_button.setToolTip ('从对应的json文件里导入动画到对应的控制器上')

        self.create_secondary_joint_button.setToolTip ('选择需要创建次级控制器的关节创建次级控制器')

        self.tool_buttons = [self.clear_keys_button , self.reset_attr_button , self.batch_Constraints_modle_button ,
                             self.batch_Constraints_joint_button , self.default_grp_button ,
                             self.control_hierarchy_button ,
                             self.save_skinWeights_button ,
                             self.load_skinWeights_button , self.select_sub_objects_button ,
                             self.print_duplicate_object_button ,
                             self.rename_duplicate_object_button , self.create_dynamic_curve_driven_button ,
                             self.snap_modle_button , self.export_animation_button , self.import_animation_button ,
                             self.create_secondary_joint_button , self.import_test_animation_button,self.skirt_ctrl_tool_btn]


    def create_layouts (self) :
        # 创建fk系统的layout
        self.fk_layout = QFormLayout ()
        self.fk_layout.addRow (self.fk_label)
        self.fk_ho_layout = QHBoxLayout ()
        self.fk_ho_layout.addWidget (self.create_fk_button)
        self.fk_ho_layout.addWidget (self.delete_fk_button)
        self.fk_ho_layout.addStretch ()
        self.fk_layout.addRow (self.fk_ho_layout)

        # 创建ik系统的layout
        self.ik_layout = QFormLayout ()
        self.ik_layout.addRow (self.ik_label)
        self.ik_layout.addRow (self.ik_start_line , self.ik_start_button)
        self.ik_layout.addRow (self.ik_end_line , self.ik_end_button)
        # self.ik_layout.addRow('控制器数量', self.ik_ctrlnumber_cbox)
        self.ik_ho_layout = QHBoxLayout ()
        self.ik_ho_layout.addWidget (self.create_ik_button)
        self.ik_ho_layout.addWidget (self.delete_ik_button)
        self.ik_ho_layout.addStretch ()
        self.ik_layout.addRow (self.ik_ho_layout)

        # 创建小工具的layout
        self.tool_layout = QGridLayout ()
        self.create_tool_layouts ()

        # 创建main_layout的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addLayout (self.fk_layout)
        self.main_layout.addStretch ()
        self.main_layout.addLayout (self.ik_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.tool_label)
        self.main_layout.addLayout (self.tool_layout)


    def create_tool_layouts (self) :
        # 添加按钮
        positions = [(i , j) for i in range (6) for j in range (3)]

        for position , button in zip (positions , self.tool_buttons) :
            self.tool_layout.addWidget (button , *position)


    def add_connnect (self) :
        """
        链接信号与槽
        """
        # fk系统的部件连接
        self.create_fk_button.clicked.connect (self.clicked_create_fk)
        self.delete_fk_button.clicked.connect (self.clicked_delete_fk)

        # ik系统的部件连接
        self.ik_start_button.clicked.connect (self.clicked_ik_start_pickup)
        self.ik_end_button.clicked.connect (self.clicked_ik_end_pickup)
        self.create_ik_button.clicked.connect (self.clicked_create_ik_ctrl)
        self.delete_ik_button.clicked.connect (self.clicked_delete_ik_ctrl)

        # 绑定小工具的部件连接
        self.add_tool_connect ()


    def add_tool_connect (self) :
        """
        连接绑定小工具的连接
        """
        self.clear_keys_button.clicked.connect (lambda *args : pipelineUtils.Pipeline.clear_keys ())

        self.reset_attr_button.clicked.connect (self.clicked_reset_attr)

        self.batch_Constraints_modle_button.clicked.connect (
            lambda *args : pipelineUtils.Pipeline.batch_Constraints_modle ())

        self.batch_Constraints_joint_button.clicked.connect (
            lambda *args : pipelineUtils.Pipeline.batch_Constraints_joint ())

        self.default_grp_button.clicked.connect (lambda *args : hierarchyUtils.Hierarchy.create_default_grp ())

        self.control_hierarchy_button.clicked.connect (lambda *args : hierarchyUtils.Hierarchy.control_hierarchy ())

        self.save_skinWeights_button.clicked.connect (self.save_skinWeights)

        self.load_skinWeights_button.clicked.connect (self.load_skinWeights)

        self.select_sub_objects_button.clicked.connect (lambda *args : hierarchyUtils.Hierarchy.select_sub_objects ())

        self.print_duplicate_object_button.clicked.connect (lambda *args : nameUtils.Name.print_duplicate_object ()
                                                            )

        self.rename_duplicate_object_button.clicked.connect (lambda *args : nameUtils.Name.rename_duplicate_object ())

        self.create_dynamic_curve_driven_button.clicked.connect (
            lambda *args : pipelineUtils.Pipeline.create_dynamic_curve_driven ())

        self.snap_modle_button.clicked.connect (lambda *args : snapUtils.Snap.push_snip ())

        self.export_animation_button.clicked.connect (self.clicked_export_animation)
        self.import_animation_button.clicked.connect (self.clicked_import_animation)
        self.create_secondary_joint_button.clicked.connect (lambda *args : jointUtils.Joint.create_secondary_joint ())

        self.import_test_animation_button.clicked.connect(self.clicked_import_test_animation_button)

        self.skirt_ctrl_tool_btn.clicked.connect(lambda *args : skirt_ctrl_tool.main())
    def clicked_export_animation (self) :
        # 连接选择控制器进行导出动画的按钮
        file = fileUtils.File ()
        file.export_animation_json ()


    def clicked_import_animation (self) :
        # 连接选择导入控制器动画的按钮
        file = fileUtils.File ()
        file.import_animation_json ()


    def save_skinWeights (self) :
        """
        保存权重
        """
        geos = cmds.ls (sl = True)
        for geo in geos :
            obj = weightsUtils.Weights (geo)
            obj.save_skinWeights ()


    def load_skinWeights (self) :
        """
        载入权重
        """
        geos = cmds.ls (sl = True)
        for geo in geos :
            obj = weightsUtils.Weights (geo)
            obj.load_skinWeights ()


    def clicked_create_fk (self) :
        objects = cmds.ls (sl = True)
        controlUtils.Control.create_fk_ctrl (objects)


    def clicked_delete_fk (self) :
        objects = cmds.ls (sl = True)
        controlUtils.Control.delete_fk_ctrl (objects)


    def clicked_ik_start_pickup (self) :
        ik_start = cmds.ls (sl = True , type = 'joint')
        if len (ik_start) != 1 :
            pm.warning ("选择了多个关节，请只选择一个关节作为ik系统的起始关节 " + ik_start)
            return
        else :
            self.ik_start_line.setText (ik_start [0])
            pm.warning ("设定了{}为ik系统的起始关节 ".format (ik_start [0]))


    def clicked_ik_end_pickup (self) :
        ik_end = cmds.ls (sl = True , type = 'joint')
        if len (ik_end) != 1 :
            pm.warning ("选择了多个关节，请只选择一个关节作为ik系统的末端关节 " + ik_end)
            return
        else :
            self.ik_end_line.setText (ik_end [0])
            pm.warning ("设定了{}为ik系统的末端关节 ".format (ik_end [0]))


    def clicked_create_ik_ctrl (self) :
        startIK_jnt = self.ik_start_line.text ()
        endIK_jnt = self.ik_end_line.text ()
        # 创建ik控制器
        controlUtils.Control.create_ik_ctrl (startIK_jnt , endIK_jnt)


    def clicked_delete_ik_ctrl (self) :
        objects = cmds.ls (sl = True)
        controlUtils.Control.delete_ik_ctrl (objects)


    def clicked_reset_attr (self) :
        nodes = cmds.ls (sl = True)
        for node in nodes :
            attrUtils.Attr.reset_attr (node)


    def clicked_import_test_animation_button (self) :
        """
        用来连接导入动作测试的按钮
        """
        # 连接选择导入控制器动画的按钮
        file = fileUtils.File ()
        file.import_test_animation_json ()


def main () :
    return Rig_Tool ()


if __name__ == "__main__" :
    app = QApplication (sys.argv)
    mainwindow = Rig_Tool ()
    mainwindow.show ()
    sys.exit (app.exec_ ())
