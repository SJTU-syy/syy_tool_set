import maya.cmds as cmds
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFileDialog

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