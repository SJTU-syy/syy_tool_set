import maya.cmds as cmds
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFileDialog


############################################################
# 约束操作
############################################################
def create_control(name, shape='circle', size=1):
    """
    创建一个控制器
    :param name: 控制器的名称
    :param shape: 控制器的形状（默认为圆形）
    :param size: 控制器的大小
    :return: 控制器的名称
    """
    if shape == 'circle':
        control = cmds.circle(name=name, radius=size)[0]
    elif shape == 'square':
        control = cmds.curve(name=name, d=1, p=[[-size, size, 0], [-size, -size, 0], [size, -size, 0], [size, size, 0], [-size, size, 0]])
    else:
        raise ValueError("Unsupported shape type")

    return control

def create_position_control(bone_name):
    """
    为给定骨骼创建位置控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_pos_ctrl", shape='circle')
    # cmds.parent(control, world=True)
    print(f'{bone_name}_pos_ctrl')
    cmds.pointConstraint(control, bone_name, maintainOffset=False)

def create_rotation_control(bone_name):
    """
    为给定骨骼创建旋转控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_rot_ctrl", shape='circle')
    # cmds.parent(control, world=True)
    print(f'{bone_name}_rot_ctrl')
    cmds.orientConstraint(control, bone_name, maintainOffset=False)

def create_scale_control(bone_name):
    """
    为给定骨骼创建缩放控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_scl_ctrl", shape='circle')
    # cmds.parent(control, world=True)
    print(f'{bone_name}_scl_ctrl')
    cmds.scaleConstraint(control, bone_name, maintainOffset=False)

def create_parent_control(bone_name):
    """
    为给定骨骼创建父控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_parent_ctrl", shape='square', size=0.5)
    # cmds.parent(control, world=True)
    print(f'{bone_name}_parent_ctrl')
    cmds.parentConstraint(control, bone_name, maintainOffset=False)

def create_Aim_control(bone_name):
    """
    为给定骨骼创建Aim控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_aim_ctrl", shape='circle')
    # cmds.parent(control, world=True)
    print(f'{bone_name}_aim_ctrl')
    cmds.aimConstraint(control, bone_name, maintainOffset=False)

############################################################
# IK操作
############################################################
def create_pole_vector_control(bone_name):
    """
    为给定骨骼创建pole vector控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_pole_ctrl", shape='circle')
    # cmds.parent(control, world=True)
    print(f'{bone_name}_pole_ctrl')
    cmds.poleVectorConstraint(control, bone_name, maintainOffset=False)

def create_ik_control(bone_name):
    """
    为给定骨骼创建ik控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_ik_ctrl", shape='circle')
    # cmds.parent(control, world=True)
    print(f'{bone_name}_ik_ctrl')
    cmds.ikHandle(name=f"{bone_name}_ik_handle", startJoint=bone_name, endEffector=f"{bone_name}_ik_ctrl", solver="ikRPsolver")

def add_biped_controllers(Tab):
    """
        为手指和头部之外的大部分关节创建控制器
    """

    # 定义需要创建控制器的骨骼名称
    bones_to_control = [
        "Root",
        "Spine1", "Chest",
        "Scapula", "Shoulder", "Elbow", "Wrist",
        "Hip", "Knee", "Ankle", "Heel", "Toes"
    ]

    # 为每个骨骼节点创建控制器
    for bone in bones_to_control:
        # 先创建位置控制器
        create_position_control(bone)
        # 然后创建旋转控制器
        create_rotation_control(bone)

    print("biped模型的主要控制器已添加")


############################################################
# 调整场景显示
############################################################

# 调整关节显示大小
def set_joint_display_size(size):
    """
    调整场景中所有关节的显示大小。

    :param size: 关节的显示大小，输入的数字必须为正数。
    """
    if size <= 0:
        cmds.warning("关节显示大小必须是正数。")
        return

    # 获取场景中所有的关节
    joints = cmds.ls(type='joint')

    if not joints:
        cmds.warning("场景中没有找到任何关节。")
        return

    # 遍历每个关节并设置显示大小
    for joint in joints:
        cmds.setAttr(f"{joint}.radius", size)

    # 确保关节的显示大小全局设置为 `Custom` 模式
    cmds.displayPref(jointSize=size)
    cmds.inViewMessage(amg=f"关节显示大小设置为: {size}", pos="midCenter", fade=True)
# 调用示例，输入你希望的关节显示大小
# set_joint_display_size(2.0)

# 切换 IK, FK, IKFK 显示
def switch_ik_fk(show_ik, show_fk, show_ikfk):
    """
    根据传入的布尔值切换 IK, FK, IKFK 的显示。

    :param show_ik: bool, True 显示 IK, False 隐藏 IK
    :param show_fk: bool, True 显示 FK, False 隐藏 FK
    :param show_ikfk: bool, True 显示 IKFK, False 隐藏 IKFK
    """
    # 假设 IK 控制器在场景中的命名规范包含 'IK'，FK 控制器包含 'FK'
    ik_controllers = cmds.ls('*IK*', type='transform')
    fk_controllers = cmds.ls('*FK*', type='transform')
    ikfk_controllers = cmds.ls('*IKFK*', type='transform')

    # 控制 IK 显示
    for ik_ctrl in ik_controllers:
        cmds.setAttr(f"{ik_ctrl}.visibility", show_ik)

    # 控制 FK 显示
    for fk_ctrl in fk_controllers:
        cmds.setAttr(f"{fk_ctrl}.visibility", show_fk)

    # 控制 IKFK 混合控制器的显示
    for ikfk_ctrl in ikfk_controllers:
        cmds.setAttr(f"{ikfk_ctrl}.visibility", show_ikfk)

    cmds.inViewMessage(amg=f"IK: {show_ik}, FK: {show_fk}, IKFK: {show_ikfk}", pos="midCenter", fade=True)

# 示例调用：显示 IK，隐藏 FK 和 IKFK
switch_ik_fk(True, False, False)
