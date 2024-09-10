import maya.cmds as cmds
import func.name as nm
import importlib
importlib.reload(nm)

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

# 镜像对象及其所有子对象
def mirror_object_and_children(source_object):
    # 获取对象及其所有子对象
    all_objects = get_object_and_children(source_object)

    # 处理变换历史
    cmds.select(all_objects)
    cmds.delete(ch=True)  # 删除变换历史

    # 处理对象及其子对象的镜像
    for obj in all_objects:
        position = cmds.xform(obj, query=True, translation=True, worldSpace=True)

        # 获取当前的关节方向
        joint_orient = cmds.getAttr(obj + ".jointOrient")[0]

        print(f"{obj} mirrored world position: {cmds.xform(obj, query=True, translation=True, worldSpace=True)}")
        print(f"{obj} mirrored local position: {cmds.xform(obj, query=True, translation=True)}")

        mirrored_position = (-position[0], position[1], position[2])
        # 镜像关节方向
        mirrored_joint_orient = (-joint_orient[0], joint_orient[1], joint_orient[2])

        # 应用变换，顺序不影响
        cmds.joint(obj, edit=True, orientation=mirrored_joint_orient)





        # 设置新的关节方向
        cmds.setAttr(obj + ".jointOrient", *mirrored_joint_orient, type="double3")


        # 打印调试信息
        print(f"{obj} mirrored world position: {cmds.xform(obj, query=True, translation=True, worldSpace=True)}")
        print(f"{obj} mirrored local position: {cmds.xform(obj, query=True, translation=True)}")

    return source_object

# 输入坐标和骨骼名称创建对称的骨骼系统
def create_symmetric_skeleton(skeleton_name, joint_positions):
    """
    创建对称的骨骼系统

    :param skeleton_name: 骨骼系统的名称
    :param joint_positions: 关节的位置列表，每个位置是一个 (x, y, z) 元组
    """
    # 创建根节点
    root_joint = cmds.joint(name=f"{skeleton_name}_Root", position=joint_positions[0])


    # 创建左侧关节
    left_joints = []
    for i, position in enumerate(joint_positions[1:]):
        joint_name = f"{skeleton_name}_L{i+1}"
        cmds.select(clear=True)  # 清空选择集，防止自动设置父子关系
        joint = cmds.joint(name=joint_name, position=position)
        left_joints.append(joint)

    # 确保左侧关节的父子关系正确
    for i in range(1, len(left_joints)):
        cmds.parent(left_joints[i], left_joints[i-1])

    # 连接根节点
    cmds.parent(left_joints[0], root_joint)

    #复制左侧关节为右侧关节
    cmds.select(clear=True)
    right_joint = cmds.duplicate(left_joints[0], name=f"{skeleton_name}_R")




    # 返回创建的骨骼系统
    return root_joint
# 示例使用
# joint_positions = [(0, 0, 0), (0, 1, 0), (0, 2, 0)]
# root_joint = create_symmetric_skeleton("MySkeleton", joint_positions)


# 输入父对象，创建对称的子对象系统
def create_symmetric(parent, is_left=True):
    """
    输入父对象，创建对称的子对象系统
    """
    # 获取父关节的子对象
    children = cmds.listRelatives(parent, children=True, fullPath=True)

    # 确保父关节只有一个子关节
    if not children or len(children) > 1:
        cmds.error("父关节必须有且只有一个子关节")
        return

    child_first = children[0]
    original_name = child_first.split("|")[-1]

    # 复制
    duplicated_nodes = cmds.duplicate(child_first, name=f"{original_name}_copy")
    if not duplicated_nodes:
        cmds.error("复制失败")
        return

    child_second = duplicated_nodes[0]  # 获取复制的第一个节点，这个是重点

    # 重命名
    child_first = nm.rename_recursive(child_first, "L")
    # 就是有返回值，就是这么干的
    child_second = cmds.rename(child_second, f"{original_name}")
    child_second = nm.rename_recursive(child_second, "R")

    # 镜像
    child_second = mirror_object_and_children(child_second)

    return parent





create_symmetric("joint1")