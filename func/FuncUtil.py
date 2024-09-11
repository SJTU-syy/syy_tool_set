import maya.cmds as cmds

# 获取对象及其所有子对象的数组
def get_object_and_children(source_object):
    """
    获取对象及其所有子对象的数组

    :param source_object: 要获取的对象名称
    :return: 包含对象及其所有子对象的数组
    """
    # 获取对象及其所有子对象
    all_objects = cmds.listRelatives(source_object, allDescendents=True, fullPath=True) or []
    #尾部插入父对象
    all_objects.append(source_object)
    #翻转数组，使其从后往前遍历
    all_objects.reverse()

    return all_objects

# 判断两个关节是否有父子关系
def are_joints_parented(parent_joint, child_joint):
    """
    判断两个关节是否有父子关系

    :param parent_joint: 父关节的名称
    :param child_joint: 子关节的名称
    :return: 如果有父子关系返回 True，否则返回 False
    """
    # 获取子关节的父节点列表
    parents = cmds.listRelatives(child_joint, parent=True) or []

    # 检查父关节是否在子关节的父节点列表中
    return parent_joint in parents