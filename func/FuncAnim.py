import maya.cmds as cmds
############################################################
# 关键帧操作
############################################################

# 自动插入关键帧
def auto_keyframe_insertion(start_frame, end_frame, interval, attributes):
    for frame in range(start_frame, end_frame + 1, interval):
        cmds.currentTime(frame, edit=True)
        for attr in attributes:
            if cmds.getAttr(attr, keyable=True):
                cmds.setKeyframe(attr)

# 重置关键帧
def reset_keyframes(objects, start_frame, end_frame):
    for obj in objects:
        cmds.cutKey(obj, time=(start_frame, end_frame), clear=True)

# 导出当前选中对象的关键帧
def export_keyframes(file_path):
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("未选择任何物体。")
        return

    keyframe_data = []

    # 遍历每个选中的物体
    for obj in selected_objects:
        key_times = cmds.keyframe(obj, query=True, timeChange=True)

        if key_times:
            for key_time in key_times:
                key_value = cmds.keyframe(obj, query=True, time=(key_time, key_time), valueChange=True)[0]
                keyframe_data.append(f"物体: {obj}, 时间: {key_time}, 值: {key_value}\n")
        else:
            keyframe_data.append(f"物体: {obj} 没有关键帧。\n")

    # 将关键帧数据写入文件
    with open(file_path, 'w') as file:
        file.writelines(keyframe_data)

    cmds.confirmDialog(title='导出完成', message=f'关键帧已导出到 {file_path}', button=['确定'])


############################################################
# 曲线操作
############################################################

#曲线编辑器
# 创建自定义曲线
def create_custom_curve(name, keyframes, values):
    curve = cmds.curve(d=1, p=[(x, y, 0) for x, y in zip(keyframes, values)])
    cmds.rename(curve, name)
    return curve
# 设置曲线关键帧
def set_curve_keyframes(curve, keyframes, values):
    cmds.select(curve)
    for frame, value in zip(keyframes, values):
        cmds.setKeyframe(curve, time=frame, value=value)

# 创建运动轨迹
def create_motion_path(joint, start_frame, end_frame):
    path = cmds.curve(d=1, p=[(0, 0, 0), (10, 10, 10)], k=[0, 1])
    motion_path = cmds.pathAnimation(joint, c=path, startTime=start_frame, endTime=end_frame)
    return motion_path



############################################################
# 动画操作
############################################################

# 简化动画曲线
def simplify_animation_curve(curve, tolerance=0.01):
    cmds.select(curve)
    cmds.keyframe(s=True, r=True, time=(1, 100))
    cmds.filterCurve(curve, threshold=tolerance)

# 镜像动画
def mirror_animation(source_joint, target_joint, start_frame, end_frame):
    # 记录源骨骼的动画
    for frame in range(start_frame, end_frame + 1):
        cmds.currentTime(frame, edit=True)
        attrs = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
        for attr in attrs:
            source_value = cmds.getAttr(f'{source_joint}.{attr}')
            cmds.setKeyframe(target_joint, attribute=attr, value=source_value)