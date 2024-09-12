import maya.cmds as cmds

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
    cmds.parent(control, world=True)
    cmds.pointConstraint(control, bone_name, maintainOffset=False)

def create_rotation_control(bone_name):
    """
    为给定骨骼创建旋转控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_rot_ctrl", shape='circle')
    cmds.parent(control, world=True)
    cmds.orientConstraint(control, bone_name, maintainOffset=False)

def create_scale_control(bone_name):
    """
    为给定骨骼创建缩放控制器
    :param bone_name: 骨骼的名称
    """
    control = create_control(name=f"{bone_name}_scale_ctrl", shape='circle')
    cmds.parent(control, world=True)
    cmds.scaleConstraint(control, bone_name, maintainOffset=False)

# # 使用示例
# bone = "your_bone_name_here"
# create_position_control(bone)
# create_rotation_control(bone)
# create_scale_control(bone)