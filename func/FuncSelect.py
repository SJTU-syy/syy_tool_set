import maya.cmds as cmds


############################################################
# 获取
############################################################

# 获取对象及其所有子对象，返回数组
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


############################################################
# 查找
############################################################

# 根据pattern内容模式匹配节点
def find_matched_nodes(joints, patterns):
    """
    查找场景中的骨骼节点，名称匹配指定模式的节点。

    :param joints: 要查找的骨骼节点列表
    :param patterns: 要匹配的模式列表，例如 ["Scapula", "Hip"]
    :return: 匹配的骨骼节点列表
    """
    # 用于存储匹配的节点
    matched_nodes = []

    for joint in joints:
        joint_name = joint.split('|')[-1]  # 去掉路径信息
        # 遍历模式列表
        for pattern in patterns:
            # print(f"正在匹配 {joint_name} 与 {pattern}")
            if joint_name in pattern:
                matched_nodes.append(joint)
                break  # 如果找到一个相同的名字，就跳出循环

    # 返回匹配的节点列表
    return matched_nodes


#TODO: 根据条件列出符合条件的节点列表，用于给前端各种勾选框用