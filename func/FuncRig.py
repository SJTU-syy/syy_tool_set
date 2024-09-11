import maya.cmds as cmds
import func.FuncName as func_nm
import func.FuncUtil as func_ut
import importlib
importlib.reload(func_nm)
importlib.reload(func_ut)




# 调用maya接口镜像关节
def mirror_joint(joint_name):
    # 确保关节存在
    if not cmds.objExists(joint_name):
        raise ValueError(f"The joint {joint_name} does not exist.")

    # 镜像关节
    mirror_joint_name = joint_name.split("|")[-1] + '_mirror'
    cmds.mirrorJoint(joint_name, mirrorBehavior=True, mirrorYZ=True)

    # 如果需要手动重命名镜像关节，可以在这里进行
    # maya2022出现的情况是，复制出来的东西会被命名成XXX+'1'
    cmds.rename(joint_name + '1', mirror_joint_name)

    return mirror_joint_name

#生成对象的左右对称骨骼系统
def create_symmetric_joint(parent, is_left=True):
    """
    输入父关节，创建对称的子对象系统
    """
    # 获取父对象的子对象
    children = cmds.listRelatives(parent, children=True, fullPath=True)

    # 确保父对象只有一个子对象
    if not children or len(children) > 1:
        cmds.error("父关节必须有且只有一个子关节")
        return

    child_first = children[0]
    original_name = child_first.split("|")[-1]

    # 镜像关节
    child_second = mirror_joint(child_first)

    print(f'child_first: {child_first}, child_second: {child_second}')


    children = cmds.listRelatives(parent, children=True, fullPath=True)
    print(f'children: {children}')



    # 重命名
    child_first = func_nm.rename_recursive(child_first, "L")
    # 需要有返回值
    child_second = cmds.rename(child_second, f"{original_name}")
    print(f'after rename child_first: {child_first}, child_second: {child_second}')
    child_second = func_nm.rename_recursive(child_second, "R")

    # 镜像


    return parent





###########################################################
###以下为非核心方法，仅供参考
###########################################################

# 镜像对象及其所有子对象的世界坐标位置
def mirror_object_and_children(source_object):
    # 获取对象及其所有子对象
    all_objects = func_ut.get_object_and_children(source_object)

    # 处理变换历史
    cmds.select(all_objects)
    cmds.delete(ch=True)  # 删除变换历史

    # 处理对象及其子对象的镜像
    for obj in all_objects:
        position = cmds.xform(obj, query=True, translation=True, worldSpace=True)
        print(f"{obj} mirrored world position: {cmds.xform(obj, query=True, translation=True, worldSpace=True)}")
        print(f"{obj} mirrored local position: {cmds.xform(obj, query=True, translation=True)}")

        mirrored_position = (-position[0], position[1], position[2])
        cmds.xform(obj, translation=mirrored_position, worldSpace=True)
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
    # 获取父对象的子对象
    children = cmds.listRelatives(parent, children=True, fullPath=True)

    # 确保父对象只有一个子对象
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
    child_first = func_nm.rename_recursive(child_first, "L")
    # 就是有返回值，就是这么干的
    child_second = cmds.rename(child_second, f"{original_name}")
    child_second = func_nm.rename_recursive(child_second, "R")

    # 镜像


    return parent




# mirror_joint("joint1")
create_symmetric_joint("joint1")