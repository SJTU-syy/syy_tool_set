import maya.cmds as cmds


def rename_recursive(obj, text, is_prefix=False, is_hierarchy=True):
    """
    递归重命名对象及其子对象

    :param obj: 要重命名的对象名称
    :param text: 要添加的前缀或后缀
    :param is_prefix: 如果为 True，则添加前缀；否则添加后缀
    :param is_hierarchy: 如果为 True，则递归重命名子对象
    """
    # 获取对象的所有直接子对象
    children = cmds.listRelatives(obj, children=True, fullPath=True) or []

    # 递归重命名子对象
    if is_hierarchy:
        for child in children:
            rename_recursive(child, text, is_prefix, is_hierarchy)

    # 重命名当前对象
    newname = rename(obj, text, is_prefix)

    return newname


def rename(obj, text, is_prefix=False):
    """
    重命名对象

    :param obj: 要重命名的对象名称
    :param text: 要添加的前缀或后缀
    :param is_prefix: 如果为 True，则添加前缀；否则添加后缀
    """
    # 获取对象最后一级名称
    obj_name = obj.split("|")[-1]

    # 生成新名称
    if is_prefix:
        new_name = f"{text}_{obj_name}"
    else:
        new_name = f"{obj_name}_{text}"

    # 获取当前对象的路径
    obj_path = cmds.ls(obj, long=True)[0]

    # 确保新名称没有冲突
    if cmds.objExists(new_name):
        cmds.error(f"命名冲突: {new_name} 已存在")
        return None

    # 重命名对象
    newobj = cmds.rename(obj_path, new_name)
    print(f"重命名 {newobj} 成功")
    return newobj
