import maya.cmds as cmds


def auto_keyframe_insertion(start_frame, end_frame, interval, attributes):
    for frame in range(start_frame, end_frame + 1, interval):
        cmds.currentTime(frame, edit=True)
        for attr in attributes:
            if cmds.getAttr(attr, keyable=True):
                cmds.setKeyframe(attr)

def mirror_animation(source_joint, target_joint, start_frame, end_frame):
    # 记录源骨骼的动画
    for frame in range(start_frame, end_frame + 1):
        cmds.currentTime(frame, edit=True)
        attrs = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
        for attr in attrs:
            source_value = cmds.getAttr(f'{source_joint}.{attr}')
            cmds.setKeyframe(target_joint, attribute=attr, value=source_value)


def create_custom_curve(name, keyframes, values):
    curve = cmds.curve(d=1, p=[(x, y, 0) for x, y in zip(keyframes, values)])
    cmds.rename(curve, name)
    return curve

def set_curve_keyframes(curve, keyframes, values):
    cmds.select(curve)
    for frame, value in zip(keyframes, values):
        cmds.setKeyframe(curve, time=frame, value=value)


def create_motion_path(joint, start_frame, end_frame):
    path = cmds.curve(d=1, p=[(0, 0, 0), (10, 10, 10)], k=[0, 1])
    motion_path = cmds.pathAnimation(joint, c=path, startTime=start_frame, endTime=end_frame)
    return motion_path



def simplify_animation_curve(curve, tolerance=0.01):
    cmds.select(curve)
    cmds.keyframe(s=True, r=True, time=(1, 100))
    cmds.filterCurve(curve, threshold=tolerance)


def reset_keyframes(objects, start_frame, end_frame):
    for obj in objects:
        cmds.cutKey(obj, time=(start_frame, end_frame), clear=True)