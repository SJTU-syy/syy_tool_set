# coding=utf-8
u"""
controlUtils：这是一个控制器模块。用来对控制器进行一系列修改的操作。

实现的功能：

设置控制器的transform节点：set_transform
设置控制器的父对象：set_parent
设置控制器的形状：set_shape
设置控制器的名字：set_name
设置控制器的颜色：set_color
设置控制器的半径：set_radius
设置控制器的旋转：set_rotate
设置控制器的偏移：set_offset
设置控制器的属性锁定和隐藏：set_locked
上传控制器形状：upload
删除控制器形状：delete_shape
镜像控制器形状：mirror
获取形状信息：get_shape
获取transform节点：get_transform
获取控制器颜色：get_color
获取控制器大小：get_radius
创建绑定用的控制器层级组：create_ctrl
创建matehuman用的控制器层级组：create_mateHuman_ctrl
创建ribbon控制器：create_ribbon

"""
from __future__ import print_function

import json
import os
from importlib import reload

import maya.cmds as cmds
import pymel.core as pm

from . import nameUtils , pipelineUtils , matehumanUtils , hierarchyUtils , attrUtils


reload (pipelineUtils)
reload (nameUtils)


class Control (object) :
    u"""
        kwargs – 修改控制器的参数
        kwargs – -n -name string 名字
        kwargs – -t -transform string/node/Control 控制器
        kwargs – -p -parent string/node 父对象
        kwargs – -s -shape data/name 形态
        kwargs – -c -color int 颜色
        kwargs – -r -radius float 半径
        kwargs – -ro -rotate [float, float,float] 旋转
        kwargs – -o -offset [float, float,float] 偏移
    """
    # 设置控制器的颜色模版
    COLORS = {'l' : (6 , 18) , 'r' : (13 , 20) , 'm' : (17 , 22)}


    def __init__ (self , *args , **kwargs) :
        self.cv = None
        self.transform = None
        self.set_transform (*args , **kwargs)
        self.set (**kwargs)


    def __repr__ (self) :
        return "{m}.{c}.(t = {t})".format (m = __name__ , c = self.__class__.__name__ ,
                                           t = self.get_transform ().name ())


    # 设置控制器属性
    def set (self , **kwargs) :
        """
        设置控制器属性
        set_parent: 设置父对象。
        set_shape: 设置形态。
        set_name: 设置名字。
        set_color: 设置颜色。
        set_radius: 设置半径。
        set_offset: 设置偏移。
        set_locked: 设置锁定状态。
        """
        self.set_parent (**kwargs)
        self.set_shape (**kwargs)
        self.set_name (**kwargs)
        self.set_color (**kwargs)
        self.set_radius (**kwargs)
        self.set_offset (**kwargs)
        self.set_locked (**kwargs)


    # 设置控制器的transform节点
    def set_transform (self , *args , **kwargs) :
        u"""
        设置控制器的transform节点
        -t -transform string/node/Control 控制器节点
        """
        t = kwargs.get ("t" , kwargs.get ("transform" , self.get_arg (args)))
        # 如果没有给定t（transform）的值，或者选择的物体没有transform节点，则创建一个transform节点
        if t is None :
            self.transform = pm.group (em = 1)
        # 如果给定了t(transfrom) 的值
        elif isinstance (t , (str , u"".__class__)) :
            # 如果t(transfrom) ，不存在于该场景
            if not pm.objExists (t) :
                pm.warning ("没有与名称符合的物体 " + t)
                self.set_transform ()
            else :
                transforms = pm.ls (t , type = "transform")
                # 如果t(transfrom)，该场景存在多个重名的物体
                if len (transforms) != 1 :
                    pm.warning ("有多个名称相同的物体 " + t)
                    self.transform = transforms [0]
                else :
                    self.transform = transforms [0]
        elif isinstance (t , Control) :
            self.transform = t.transform

        # 检查有没有nodeType这个属性或者是nodeType这个属性是否为transform
        elif hasattr (t , "nodeType") and t.nodeType () == "transform" :
            self.transform = t


    # 设置控制器的父对象
    def set_parent (self , *args , **kwargs) :
        u"""
        设置控制器的父对象
        -p -parent string/node 父对象
        """
        parent = kwargs.get ("p" , kwargs.get ("parent" , self.get_arg (args)))
        if parent :
            self.get_transform ().setParent (parent)
            try :

                self.get_transform ().t.set (0 , 0 , 0)
                self.get_transform ().r.set (0 , 0 , 0)
                self.get_transform ().s.set (1 , 1 , 1)
            except (RuntimeError , UnicodeEncodeError) :
                pass


    # 设置控制器的形状
    def set_shape (self , *args , **kwargs) :
        u"""
        设置控制器的形状
        -s -shape data/name 形态
        """
        shape = kwargs.get ("s" , kwargs.get ("shape" , self.get_arg (args)))
        color = self.get_color ()
        radius = self.get_radius ()
        if shape is None :
            return
        if isinstance (shape , list) :
            shapes = self.get_transform ().getShapes ()
            if shapes :
                pm.delete (shapes)
            for data in shape :
                p = [[data ["points"] [i + j] for j in range (3)] for i in range (0 , len (data ["points"]) , 3)]
                if data ["periodic"] :
                    p = p + p [:data ["degree"]]
                curve = pm.curve (degree = data ["degree"] ,
                                  knot = data ["knot"] ,
                                  periodic = data ["periodic"] ,
                                  p = p)
                curve.getShape ().setParent (self.get_transform () , s = 1 , add = 1)
                curve.getShape ().rename (self.get_transform ().name ().split ("|") [-1] + "Shape")
                pm.delete (curve)
            self.set_color (color)
            self.set_radius (radius)
        elif isinstance (shape , (str , bool)) :
            # elif isinstance(shape , (str , unicode)) :
            data_file = os.path.abspath (__file__ + "/../../tools/image/{s}.json".format (s = shape))
            if not os.path.isfile (data_file) :
                pm.warning (u"找不到这个文件 " + data_file)
                return
            with open (data_file , "r") as fp :
                self.set_shape (s = json.load (fp))


    # 设置控制器的名称
    def set_name (self , *args , **kwargs) :
        u"""
        设置控制器的名称
        """
        n = kwargs.get ("n" , kwargs.get ("name" , self.get_arg (args)))
        if n is None :
            return
        self.get_transform ().rename (n)
        for s in self.get_transform ().getShapes () :
            s.rename (n + "Shape")


    # 设置控制器的颜色
    def set_color (self , *args , **kwargs) :
        u"""
        设置控制器的颜色
        -c -color int 颜色
        """
        color = kwargs.get ("c" , kwargs.get ("color" , self.get_arg (args)))
        if color is None :
            return
        for shape in self.get_transform ().getShapes () :
            # 如果形状节点的节点类型不是曲线，则取消设置颜色
            if shape.nodeType () != "nurbsCurve" :
                continue
            shape.overrideEnabled.set (True)
            shape.overrideColor.set (color)


    # 设置控制器的半径大小
    def set_radius (self , *args , **kwargs) :
        u"""
        设置控制器的半径
        -r -radius (float) :半径
        """
        radius = kwargs.get ('r' , kwargs.get ('radius' , self.get_arg (args)))
        if radius is None :
            return
        points = [self.get_curve_shape_points (shape) for shape in self.get_transform ().getShapes ()]
        points = [[[ps [i + j] for j in range (3)] for i in range (0 , len (ps) , 3)] for ps in points]
        lengths = [self.get_length (p , [0 , 0 , 0]) for ps in points for p in ps]
        origin_radius = max (lengths) if lengths else 0.0
        scale = radius / origin_radius
        for shape , ps in zip (self.get_transform ().getShapes () , points) :
            for p , cv in zip (ps , shape.cv) :
                pm.xform (cv , t = [xyz * scale for xyz in p])


    # 设置控制器的选择X
    def set_rotateX (self , **kwargs) :
        rotateX = kwargs.get ('rx' , kwargs.get ('rotateX' , 0))  # type: int
        shape_node = cmds.listRelatives ('{}'.format (self.get_transform ()) , shapes = True) [0]
        points = '{}'.format (shape_node) + ".cv[0:700000]"
        cmds.rotate (rotateX , 0 , 0 , points)


    # 设置控制器的选择Y
    def set_rotateY (self , **kwargs) :
        rotateY = kwargs.get ('ry' , kwargs.get ('rotateY' , 0))  # type: int
        shape_node = cmds.listRelatives ('{}'.format (self.get_transform ()) , shapes = True) [0]
        points = '{}'.format (shape_node) + ".cv[0:700000]"
        cmds.rotate (0 , rotateY , 0 , points)


    # 设置控制器的旋转Z
    def set_rotateZ (self , **kwargs) :
        rotateZ = kwargs.get ('rz' , kwargs.get ('rotateZ' , 0))  # type: int
        shape_node = cmds.listRelatives ('{}'.format (self.get_transform ()) , shapes = True) [0]
        points = '{}'.format (shape_node) + ".cv[0:700000]"
        cmds.rotate (0 , 0 , rotateZ , points)


    # 设置控制器的偏移
    def set_offset (self , *args , **kwargs) :
        u"""
        设置偏移
        kwargs – -o -offset [float, float,float] 偏移
        """
        offset = kwargs.get ("o" , kwargs.get ("offset" , self.get_arg (args)))
        if offset is None :
            return
        points = [self.get_curve_shape_points (shape) for shape in self.get_transform ().getShapes ()]
        points = [[[ps [i + j] for j in range (3)] for i in range (0 , len (ps) , 3)] for ps in points]
        for shape , ps in zip (self.get_transform ().getShapes () , points) :
            for p , cv in zip (ps , shape.cv) :
                pm.xform (cv , t = [p_xyz + o_xyz for p_xyz , o_xyz in zip (p , offset)])


    # 设置控制器的锁定
    def set_locked (self , *args , **kwargs) :
        pass


    # 上传控制器形状的信息到指定路径，并截取控制器形状的图像。
    def upload (self) :
        u"""
        上传控制器形状的信息到指定路径，并截取控制器形状的图像。
        """
        data_path = os.path.abspath (__file__ + "/../../tools/image")
        if not os.path.isdir (data_path) :
            pm.warning (u"没有找到这个路径" + data_path)
            return
        data_file = os.path.join (data_path , self.get_transform ().name ().split ("|") [-1] + ".json")
        # 打开并写入带有形状信息的date_file文件，open函数的参数有file_name，access_mode 和 buffering
        ##file_name：file_name变量是一个包含了你要访问的文件名称的字符串值。
        ##access_mode：access_mode决定了打开文件的模式：只读，写入，追加等。所有可取值见如下的完全列表。这个参数是非强制的，
        ## 默认文件访问模式为只读(r)。写入为(w)
        ##buffering:如果buffering的值被设为0，就不会有寄存。如果buffering的值取1，访问文件时会寄存行。
        ##如果将buffering的值设为大于1的整数，表明了这就是的寄存区的缓冲大小。如果取负值，寄存区的缓冲大小则为系统默认。
        with open (data_file , 'w') as fp :
            json.dump (self.get_shape () , fp , indent = 4)

        # 在视图面板中隐藏所有场景信息
        for hud in pm.headsUpDisplay (listHeadsUpDisplays = 1) :
            pm.headsUpDisplay (hud , edit = 1 , vis = False)

        # 创建一个撕下副本的面板用于截图控制器形状，如果创建的撕下副本的面板存在则关闭后重新开启
        panel = 'control_model_panel'
        if not pm.modelPanel (panel , exists = True) :
            pm.modelPanel (panel , tearOff = True , tearOffCopy = 1)

        # 关闭撕下副本视图中所有对象的显示，打开撕下副本视图的 nurbs 曲线显示，关闭撕下副本视图的网格显示。
        pm.modelEditor (panel , edit = 1 , allObjects = 0 , nurbsCurves = 1 , grid = 0)

        # 调整撕下副本视图的焦距，按键F
        pm.setFocus (panel)

        # 复制一个临时的用于截图的控制器，控制器的位置在原点中心
        temp = Control ()
        temp.set_shape (s = self.get_shape ())
        pm.select (temp.get_transform ())

        # 设置用来截图的摄影机的拍摄角度，将摄影机移动到选定对象的中心，指定应设置摄影机位置之间的过渡动画。
        pm.setAttr ('persp.rotate' , -27.938 , 45 , 0)
        pm.viewFit ('persp' , animate = 0)

        # 撕下副本面板开启隔离选择模式，将刚刚选择的需要截图的控制器添加到要显示的对象集中
        pm.isolateSelect (panel , state = 1)
        pm.isolateSelect (panel , addSelected = True)

        # 设定拍屏截图的文件名称和文件路径和拍屏的参数设置
        jpg_path = os.path.join (data_path , self.get_transform ().split ("|") [-1])
        file_name = pm.playblast (format = "image" , filename = jpg_path , c = "jpg" , widthHeight = [256 , 256] ,
                                  startTime = 0 , endTime = 0 , viewer = False , percent = 100 , quality = 100 ,
                                  framePadding = 1)

        # 修改拍屏截图后的保存的文件名称，如果有相同名称的文件存在则删除过去的截图文件
        if os.path.isfile (file_name.replace ("####" , "0")) :
            if os.path.isfile (file_name.replace ("####." , "")) :
                os.remove (file_name.replace ("####." , ""))
            os.rename (file_name.replace ("####" , "0") , file_name.replace ("####." , ""))

        # 关闭撕下副本面板
        if pm.modelPanel (panel , ex = 1) :
            pm.deleteUI (panel , panel = True)

        # 删除用来截图的控制器
        pm.delete (temp.get_transform ())


    # 镜像控制器，将指定控制器的形状信息镜像到当前控制器上。
    def mirror (self , other) :
        u"""
        镜像控制器，将指定控制器的形状信息镜像到当前控制器上。
        :param other: 镜像控制器的目标
        :return:
        """
        self.set_shape (s = other.get_shape ())
        for src_shape , dst_shape in zip (self.get_transform ().getShapes () , other.get_transform ().getShapes ()) :
            for src_cv , dst_cv in zip (src_shape.cv , dst_shape.cv) :
                point = pm.xform (dst_cv , q = 1 , t = 1 , ws = 1)
                point [0] = -point [0]
                pm.xform (src_cv , t = point , ws = 1)


    # 获取控制器形状的数据
    def get_shape (self) :
        u"""

        :return: data
        控制器形状的数据
        """
        return [dict (points = self.get_curve_shape_points (shape) ,
                      degree = shape.degree () ,
                      periodic = shape.form () == 3 ,
                      knot = shape.getKnots ())
                for shape in self.get_transform ().getShapes ()]


    # 获取控制器的transform节点
    def get_transform (self) :
        u"""
         -t -transform string/node/Control 控制器
        :return: transform node
        返回控制器的transform节点
        """
        return self.transform


    # 获取控制器的颜色
    def get_color (self) :
        """
        获得控制器的颜色
        -c - color int : 控制器颜色
        :return:
        """
        c = 0
        for shape in self.get_transform ().getShapes () :
            c = shape.overrideColor.get ()
        return c


    # 获取控制器的半径大小
    def get_radius (self) :
        """
        获得控制器的大小
        -r - radius int : 控制器大小
        :return:
        """
        if len (self.get_transform ().getShapes ()) == 0 :
            return self.get_soft_radius ()
        points = [self.get_curve_shape_points (shape) for shape in self.get_transform ().getShapes ()]
        points = [[[ps [i + j] for j in range (3)] for i in range (0 , len (ps) , 3)] for ps in points]
        lengths = [self.get_length (p , [0 , 0 , 0]) for ps in points for p in ps]
        radius = max (lengths)
        return radius


    # 基于参数ctrl_side_name_index创建控制器
    @staticmethod
    def create_ctrl (name , shape , radius , axis , pos , parent = None) :
        u"""基于参数ctrl_side_name_index创建控制器

        Args:
            name(str/None): 控制器的名称.
            # side (str/None): 控制器的边.
            # description (str): 控制器的描述.
            # index (int/None): 控制器的编号.
            shape (str): 控制器的形状.
            radius(float):控制器形状的大小.
            pos(str) : 被吸附物体的位置
            axis (str): 控制器的朝向. 'X+'/'X-'/'Y+'/'Y-'/'Z+'/'Z-'
            lock_attrs (list): 要锁定的控制器属性.
            parent (str/None): 控制器的父层级.
            animation_set (str/None): 动画控制器集.



        Raises:
            ValueError: 如果控制器名称已存在.

        Returns:
            str: 控制器的名称

        """

        global ctrl_color , sub_color
        name_obj = nameUtils.Name (name = name)
        name_obj.decompose ()
        # 获得控制器边的参数
        if name_obj.side == 'l' or 'L' :
            ctrl_color = 6
            sub_color = 18
        elif name_obj.side == 'r' or 'R' :
            ctrl_color = 13
            sub_color = 20
        elif name_obj.side == 'm' or 'M' :
            ctrl_color = 17
            sub_color = 22

        if cmds.objExists (name_obj.name) :
            raise ValueError (u'{} 在场景中已存在'.format (name_obj.name))
        else :
            ctrl = Control (n = name_obj.name , s = shape , r = radius)
            ctrl_transform = '{}'.format (ctrl.transform)
            # 复制ctrl作为次级控制器
            sub_obj = nameUtils.Name (name = name)
            sub_obj.description = sub_obj.description + 'Sub'
            sub_ctrl = Control (n = sub_obj.name , s = shape , r = radius * 0.7)
            sub_ctrl.set_parent (ctrl.transform)
            # 设置控制器形状方向
            if axis == 'X+' :
                ctrl.set_rotateX (rx = 90)
                sub_ctrl.set_rotateX (rx = 90)
            elif axis == 'X-' :
                ctrl.set_rotateX (rx = -90)
                sub_ctrl.set_rotateX (rx = -90)
            elif axis == 'Y+' :
                ctrl.set_rotateY (ry = 90)
                sub_ctrl.set_rotateY (ry = 90)
            elif axis == 'Y-' :
                ctrl.set_rotateY (ry = -90)
                sub_ctrl.set_rotateY (ry = -90)
            elif axis == 'Z+' :
                ctrl.set_rotateZ (rz = 90)
                sub_ctrl.set_rotateZ (rz = 90)
            elif axis == 'Z-' :
                ctrl.set_rotateZ (rz = -90)
                sub_ctrl.set_rotateZ (rz = -90)

            # 设置颜色
            ctrl.set (c = ctrl_color)
            sub_ctrl.set (c = sub_color)
            # 添加上层层级组
            offset_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = ctrl_transform , grp_name = '{}'.format (name.replace ('ctrl' , 'offset')) ,
                world_orient = False)
            connect_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = offset_grp , grp_name = offset_grp.replace ('offset' , 'connect') , world_orient = False)
            sapce_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = connect_grp , grp_name = offset_grp.replace ('offset' , 'space') , world_orient = False)
            driven_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = sapce_grp , grp_name = connect_grp.replace ('connect' , 'driven') , world_orient = False)
            zero_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = driven_grp , grp_name = driven_grp.replace ('driven' , 'zero') , world_orient = False)

            # 创建output层级组
            output = cmds.createNode ('transform' , name = name.replace ('ctrl' , 'output') , parent = ctrl_transform)

            # 连接次级控制器的属性
            cmds.connectAttr (sub_ctrl.transform + '.translate' , output + '.translate')
            cmds.connectAttr (sub_ctrl.transform + '.rotate' , output + '.rotate')
            cmds.connectAttr (sub_ctrl.transform + '.scale' , output + '.scale')
            cmds.connectAttr (sub_ctrl.transform + '.rotateOrder' , output + '.rotateOrder')

            # # 添加次级控制器的属性控制在控制器上
            cmds.addAttr (ctrl_transform , longName = 'subCtrlVis' , attributeType = 'bool')
            cmds.setAttr (ctrl_transform + '.subCtrlVis' , channelBox = True)

            # 连接次级控制器的显示
            cmds.connectAttr (ctrl_transform + '.subCtrlVis' , sub_ctrl.transform + '.visibility')

            # 锁定并且隐藏不需要的属性
            attrUtils.Attr.lock_and_hide_attrs (obj = ctrl_transform , attrs_list = ['rotateOrder'] , lock = False ,
                                                hide = False)

            # 吸附到对应的位置
            if pos :
                cmds.matchTransform (zero_grp , pos , position = True , rotation = True , scale = True , piv = True)
            #
            # 做父子层级
            if parent :
                hierarchyUtils.Hierarchy.parent (child_node = zero_grp , parent_node = parent)

            #
            # 将控制器添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (ctrl_transform ,
                                               set_name = '{}_{}_ctrl_set'.format (name_obj.side ,
                                                                                   name_obj.description) ,
                                               set_parent = 'ctrl_set')

            pipelineUtils.Pipeline.create_set (sub_ctrl.transform ,
                                               set_name = '{}_{}_ctrl_set'.format (name_obj.side ,
                                                                                   name_obj.description) ,
                                               set_parent = 'ctrl_set')

        return name


    # 基于参数ctrl_side_name_index创建mateHuman的控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_mateHuman_ctrl (jnt_name , type , shape , radius , axis , pos , parent = None) :
        u"""基于参数ctrl_side_name_index创建mateHuman的控制器

        Args:
            jnt_name(str/None): 需要创建控制器的关节名称.
            type(str/None): 控制器的类型.
            # side (str/None): 控制器的边.
            # description (str): 控制器的描述.
            # index (int/None): 控制器的编号.
            shape (str): 控制器的形状.
            radius(float):控制器形状的大小.
            pos(str) : 被吸附物体的位置
            axis (str): 控制器的朝向. 'X+'/'X-'/'Y+'/'Y-'/'Z+'/'Z-'
            lock_attrs (list): 要锁定的控制器属性.
            parent (str/None): 控制器的父层级.
            animation_set (str/None): 动画控制器集.



        Raises:
            ValueError: 如果控制器名称已存在.

        Returns:
            str: 控制器的名称

        """

        global ctrl_color , sub_color
        name_obj = matehumanUtils.MateHuman (name = jnt_name)
        # 获得控制器边的参数
        if name_obj.side == 'l' :
            ctrl_color = 6
            sub_color = 18
        elif name_obj.side == 'r' :
            ctrl_color = 13
            sub_color = 20
        elif name_obj.side == 'm' :
            ctrl_color = 17
            sub_color = 22
        ctrl_name = type + '_' + name_obj.name
        if cmds.objExists (ctrl_name) :
            raise ValueError (u'{} 在场景中已存在'.format (ctrl_name))
        else :
            ctrl = Control (n = ctrl_name , s = shape , r = radius)
            ctrl_transform = '{}'.format (ctrl.transform)
            # 制作次级控制器
            sub_ctrl_name = type + 'sub_' + name_obj.name
            sub_ctrl = Control (n = sub_ctrl_name , s = shape , r = radius * 0.7)
            sub_ctrl.set_parent (ctrl.transform)
            # 设置控制器形状方向
            if axis == 'X+' :
                ctrl.set_rotateX (rx = 90)
                sub_ctrl.set_rotateX (rx = 90)
            elif axis == 'X-' :
                ctrl.set_rotateX (rx = -90)
                sub_ctrl.set_rotateX (rx = -90)
            elif axis == 'Y+' :
                ctrl.set_rotateY (ry = 90)
                sub_ctrl.set_rotateY (ry = 90)
            elif axis == 'Y-' :
                ctrl.set_rotateY (ry = -90)
                sub_ctrl.set_rotateY (ry = -90)
            elif axis == 'Z+' :
                ctrl.set_rotateZ (rz = 90)
                sub_ctrl.set_rotateZ (rz = 90)
            elif axis == 'Z-' :
                ctrl.set_rotateZ (rz = -90)
                sub_ctrl.set_rotateZ (rz = -90)

            # 设置颜色
            ctrl.set (c = ctrl_color)
            sub_ctrl.set (c = sub_color)
            # 添加上层层级组
            offset_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = ctrl_transform , grp_name = '{}'.format (ctrl_name.replace ('ctrl' , 'offset')) ,
                world_orient = False)
            connect_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = offset_grp , grp_name = offset_grp.replace ('offset' , 'connect') , world_orient = False)
            sapce_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = connect_grp , grp_name = connect_grp.replace ('connect' , 'space') , world_orient = False)
            driven_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = sapce_grp , grp_name = sapce_grp.replace ('space' , 'driven') , world_orient = False)
            zero_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = driven_grp , grp_name = driven_grp.replace ('driven' , 'zero') , world_orient = False)

            # 创建output层级组
            output = cmds.createNode ('transform' , name = ctrl_name.replace ('ctrl' , 'output') ,
                                      parent = ctrl_transform)

            # 连接次级控制器的属性
            cmds.connectAttr (sub_ctrl.transform + '.translate' , output + '.translate')
            cmds.connectAttr (sub_ctrl.transform + '.rotate' , output + '.rotate')
            cmds.connectAttr (sub_ctrl.transform + '.scale' , output + '.scale')
            cmds.connectAttr (sub_ctrl.transform + '.rotateOrder' , output + '.rotateOrder')

            # # 添加次级控制器的属性控制在控制器上
            cmds.addAttr (ctrl_transform , longName = 'subCtrlVis' , attributeType = 'bool')
            cmds.setAttr (ctrl_transform + '.subCtrlVis' , channelBox = True)

            # 连接次级控制器的显示
            cmds.connectAttr (ctrl_transform + '.subCtrlVis' , sub_ctrl.transform + '.visibility')

            # 锁定并且隐藏不需要的属性
            attrUtils.Attr.lock_and_hide_attrs (obj = ctrl_transform , attrs_list = ['rotateOrder'] , lock = False ,
                                                hide = False)
            # attrUtils.Attr.lock_and_hide_attrs(obj = ctrl_transform, attrs_list = attrs_list, lock = True,
            # hide = True)

            # 吸附到对应的位置
            if pos :
                cmds.matchTransform (zero_grp , pos , position = True , rotation = True , scale = True)
            #
            # 做父子层级
            if parent :
                hierarchyUtils.Hierarchy.parent (child_node = zero_grp , parent_node = parent)

            #
            # 将控制器添加到对应的选择集
            animation_ctrls_set = 'ctrl_set'
            if not cmds.objExists (animation_ctrls_set) or cmds.nodeType (animation_ctrls_set) != 'objectSet' :
                animation_ctrls_set = cmds.sets (name = animation_ctrls_set , empty = True)
                cmds.sets ('{}'.format (ctrl.transform) , edit = True , forceElement = animation_ctrls_set)
            else :
                cmds.sets ('{}'.format (ctrl.transform) , edit = True , forceElement = animation_ctrls_set)

        return ctrl_name


    # 基于参数name, shape , radius , axis , pos , parent = None,创建通用的控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_current_ctrl (ctrl_name , shape , radius , axis , pos , parent = None) :
        u"""基于参数name, shape , radius , axis , pos , parent = None,创建通用的控制器

        Args:
            ctrl_name(str/None): 控制器的名称.
            shape (str): 控制器的形状.
            radius(float):控制器形状的大小.
            pos(str) : 被吸附物体的位置
            axis (str): 控制器的朝向. 'X+'/'X-'/'Y+'/'Y-'/'Z+'/'Z-'
            lock_attrs (list): 要锁定的控制器属性.
            parent (str/None): 控制器的父层级.
            animation_set (str/None): 动画控制器集.



        Raises:
            ValueError: 如果控制器名称已存在.

        Returns:
            str: 控制器的名称

        """
        ctrl_color = 17
        sub_color = 22
        if cmds.objExists (ctrl_name) :
            raise ValueError (u'{} 在场景中已存在'.format (ctrl_name))
        else :
            ctrl = Control (n = ctrl_name , s = shape , r = radius)
            # 复制ctrl作为次级控制器
            sub_ctrl_name = ctrl_name + 'Sub'
            sub_ctrl = Control (n = sub_ctrl_name , s = shape , r = radius * 0.7)
            sub_ctrl.set_parent (ctrl.transform)
            # 设置控制器形状方向
            if axis == 'X+' :
                ctrl.set_rotateX (rx = 90)
                sub_ctrl.set_rotateX (rx = 90)
            elif axis == 'X-' :
                ctrl.set_rotateX (rx = -90)
                sub_ctrl.set_rotateX (rx = -90)
            elif axis == 'Y+' :
                ctrl.set_rotateY (ry = 90)
                sub_ctrl.set_rotateY (ry = 90)
            elif axis == 'Y-' :
                ctrl.set_rotateY (ry = -90)
                sub_ctrl.set_rotateY (ry = -90)
            elif axis == 'Z+' :
                ctrl.set_rotateZ (rz = 90)
                sub_ctrl.set_rotateZ (rz = 90)
            elif axis == 'Z-' :
                ctrl.set_rotateZ (rz = -90)
                sub_ctrl.set_rotateZ (rz = -90)

            # 设置颜色
            ctrl.set (c = ctrl_color)
            sub_ctrl.set (c = sub_color)
            # 添加上层层级组
            offset_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = ctrl_name , grp_name = '{}'.format (ctrl_name.replace ('ctrl' , 'offset')) ,
                world_orient = False)
            connect_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = offset_grp , grp_name = offset_grp.replace ('offset' , 'connect') , world_orient = False)
            sapce_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = connect_grp , grp_name = offset_grp.replace ('offset' , 'space') , world_orient = False)
            driven_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = sapce_grp , grp_name = connect_grp.replace ('connect' , 'driven') , world_orient = False)
            zero_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = driven_grp , grp_name = driven_grp.replace ('driven' , 'zero') , world_orient = False)

            # 创建output层级组
            output = cmds.createNode ('transform' , name = ctrl_name.replace ('ctrl' , 'output') , parent = ctrl_name)

            # 连接次级控制器的属性
            cmds.connectAttr (sub_ctrl.transform + '.translate' , output + '.translate')
            cmds.connectAttr (sub_ctrl.transform + '.rotate' , output + '.rotate')
            cmds.connectAttr (sub_ctrl.transform + '.scale' , output + '.scale')
            cmds.connectAttr (sub_ctrl.transform + '.rotateOrder' , output + '.rotateOrder')

            # # 添加次级控制器的属性控制在控制器上
            cmds.addAttr (ctrl_name , longName = 'subCtrlVis' , attributeType = 'bool')
            cmds.setAttr (ctrl_name + '.subCtrlVis' , channelBox = True)

            # 连接次级控制器的显示
            cmds.connectAttr (ctrl_name + '.subCtrlVis' , sub_ctrl.transform + '.visibility')

            # 锁定并且隐藏不需要的属性
            attrUtils.Attr.lock_and_hide_attrs (obj = ctrl_name , attrs_list = ['rotateOrder'] , lock = False ,
                                                hide = False)

            # 吸附到对应的位置
            if pos :
                cmds.matchTransform (zero_grp , pos , position = True , rotation = True , scale = True , piv = True)
            #
            # 做父子层级
            if parent :
                hierarchyUtils.Hierarchy.parent (child_node = zero_grp , parent_node = parent)

            #
            # 将控制器添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (ctrl_name ,
                                               set_name = '{}_ctrl_set'.format (ctrl.transform) ,
                                               set_parent = 'ctrl_set')

            pipelineUtils.Pipeline.create_set (sub_ctrl.transform ,
                                               set_name = '{}_ctrl_set'.format (sub_ctrl.transform) ,
                                               set_parent = 'ctrl_set')


    # 创建fk控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_fk_ctrl (objects) :
        parent = None
        for object in objects :
            ctrl_name = 'ctrl_{}'.format (object)
            ctrl = Control.create_current_ctrl (ctrl_name , shape = 'hexagon' ,
                                                radius = 4 ,
                                                axis = 'Z+' , pos = object ,
                                                parent = parent)
            # 制作约束
            pipelineUtils.Pipeline.create_constraint (driver = ctrl_name.replace ('ctrl' , 'output') , driven = object ,
                                                      point_value = False , orient_value = False , parent_value = True ,
                                                      scale_value = True ,
                                                      mo_value = True)
            # 指定关节的父层级为上一轮创建出来的控制器层级组
            parent = ctrl_name.replace ('ctrl' , 'output')
        cmds.warning ('创建了{}的fk链条'.format (objects))


    # 删除fk控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def delete_fk_ctrl (objects) :
        for object in objects :
            zero_name = 'zero_{}'.format (object)
            try :
                cmds.delete (zero_name)
                cmds.warning ('已经删除了{}的fk链条'.format (objects))
            except :
                # 已经被删除的情况就返回
                return


    # 创建ik控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_ik_ctrl (startIK_jnt , endIK_jnt) :
        u"""
        创建IKspine链的控制器绑定
        Args:
            startjnt(str):ik关节链条的起始关节
            endIK_jnt(bool):ik关节链条的结束关节
            ctrl_number(int):控制器的数量

        Returns: ik_ctrl_grp ：IK控制器的最顶层

        """
        # 获取startjnt底下所有的子物体关节作为列表
        startjnt_child_list = hierarchyUtils.Hierarchy.get_child_object (startIK_jnt , type = 'joint')
        # 获取endIK_jnt在这个关节列表里的索引值
        enjnt_index = startjnt_child_list.index (endIK_jnt)
        # ik关节链则是从0到endIK_jnt关节索引值
        ik_chain = startjnt_child_list [0 :enjnt_index]

        # 创建ik关节链条曲线
        ik_chain_crv = pipelineUtils.Pipeline.create_curve_on_joints (jnt_list = ik_chain ,
                                                                      curve = 'crvIKspine_' + ik_chain [0] ,
                                                                      degree = 3
                                                                      )
        cmds.setAttr (ik_chain_crv + '.visibility' , 0)

        # 创建开始的IK控制器
        startIK_crv_jnt = cmds.createNode ('joint' , name = 'crvjnt_' + startIK_jnt)
        cmds.matchTransform (startIK_crv_jnt , startIK_jnt , position = True , rotation = True , scale = True)

        startIK_ctrl = 'ctrl_' + startIK_jnt
        startIK_ctrl_obj = Control.create_current_ctrl (startIK_ctrl , shape = 'hexagon' ,
                                                        radius = 8 ,
                                                        axis = 'Z+' ,
                                                        pos = startIK_jnt , parent = None)
        startIK_ctrl_output = startIK_ctrl.replace ('ctrl_' , 'output_')
        startIK_zero = startIK_ctrl.replace ('ctrl_' , 'zero_')
        cmds.parent (startIK_crv_jnt , startIK_ctrl_output)
        cmds.setAttr (startIK_crv_jnt + '.visibility' , 0)

        # 创建尾端的ik控制器
        endIK_crv_jnt = cmds.createNode ('joint' , name = 'crvjnt_' + endIK_jnt)
        cmds.matchTransform (endIK_crv_jnt , endIK_jnt , position = True , rotation = True , scale = True)
        endIK_ctrl = 'ctrl_' + endIK_jnt
        endIK_ctrl_obj = Control.create_current_ctrl (endIK_ctrl , shape = 'Cube' , radius = 4 , axis = 'Y+' ,
                                                      pos = endIK_jnt , parent = None)
        endIK_ctrl_output = endIK_ctrl.replace ('ctrl_' , 'output_')
        endIK_zero = endIK_ctrl.replace ('ctrl_' , 'zero_')
        cmds.parent (endIK_crv_jnt , endIK_ctrl_output)
        cmds.setAttr (endIK_crv_jnt + '.visibility' , 0)

        #
        # 创建中间的ik控制器
        midIK_jnt = ik_chain [len (ik_chain) // 2]
        midIK_crv_jnt = cmds.createNode ('joint' , name = 'crvjnt_' + midIK_jnt)
        cmds.matchTransform (midIK_crv_jnt , midIK_jnt , position = True , rotation = True , scale = True)
        midIK_ctrl = 'ctrl_' + midIK_jnt
        midIK_ctrl_obj = Control.create_current_ctrl (midIK_ctrl , shape = 'Cube' , radius = 4 , axis = 'Y+' ,
                                                      pos = midIK_jnt , parent = None)
        midIK_ctrl_output = midIK_ctrl.replace ('ctrl_' , 'output_')
        cmds.parent (midIK_crv_jnt , midIK_ctrl_output)
        cmds.setAttr (midIK_crv_jnt + '.visibility' , 0)
        midIK_zero = midIK_ctrl.replace ('ctrl_' , 'zero_')

        # 曲线关节对ikspine曲线进行蒙皮
        cmds.skinCluster (startIK_crv_jnt , midIK_crv_jnt , endIK_crv_jnt , ik_chain_crv , tsb = True)

        # 曲线对ik关节做ik样条线手柄
        spine_ikhandle_node = \
            cmds.ikHandle (curve = ik_chain_crv , startJoint = ik_chain [0] , endEffector = ik_chain [-1] ,
                           solver = 'ikSplineSolver' , createCurve = 0 ,
                           name = 'ikhandle_' + startIK_jnt) [0]

        # 创建loc来制作ikhandle的横向旋转
        startIK_loc = cmds.spaceLocator (name = 'loc_' + startIK_jnt) [0]
        endIK_loc = cmds.spaceLocator (name = 'loc_' + endIK_jnt) [0]

        cmds.matchTransform (startIK_loc , startIK_jnt , position = True , rotation = True , scale = True)
        cmds.parent (startIK_loc , startIK_ctrl_output)
        cmds.matchTransform (endIK_loc , endIK_jnt , position = True , rotation = True , scale = True)
        cmds.parent (endIK_loc , endIK_ctrl_output)

        # 设置ikhandle的高级扭曲属性用来设置横向旋转
        cmds.setAttr (spine_ikhandle_node + '.dTwistControlEnable' , 1)
        cmds.setAttr (spine_ikhandle_node + '.dWorldUpType' , 4)
        cmds.connectAttr (startIK_loc + '.worldMatrix[0]' , spine_ikhandle_node + '.dWorldUpMatrix')
        cmds.connectAttr (endIK_loc + '.worldMatrix[0]' , spine_ikhandle_node + '.dWorldUpMatrixEnd')
        cmds.setAttr (spine_ikhandle_node + '.visibility' , 0)

        # 整理层级结构
        ik_ctrl_grp = cmds.createNode ('transform' , name = "grpIKspine_" + ik_chain [0])
        cmds.parent (spine_ikhandle_node , ik_chain_crv , startIK_zero , midIK_zero , endIK_zero , ik_ctrl_grp)

        # 添加拉伸效果
        # 获取ikspine曲线的形状节点
        ik_chain_crv_shape = cmds.listRelatives (ik_chain_crv , shapes = True) [0]

        # 创建curveinfo节点来获取ikspine曲线的长度
        curveInfo_node = cmds.createNode ('curveInfo' , name = 'crvInfo_' + ik_chain_crv)
        cmds.connectAttr (ik_chain_crv_shape + '.worldSpace' , curveInfo_node + '.inputCurve')
        ik_chain_crv_value = cmds.getAttr (curveInfo_node + '.arcLength')

        # 创建一个相加节点来获取ikspine曲线变换的数值
        add_curveInfo_node = cmds.createNode ('addDoubleLinear' , name = 'add_' + ik_chain_crv)
        cmds.connectAttr (curveInfo_node + '.arcLength' , add_curveInfo_node + '.input1')
        cmds.setAttr (add_curveInfo_node + '.input2' , ik_chain_crv_value * -1)

        # 创建一个相乘节点，来将变换的数值平均分配给每个关节
        mult_curveInfo_node = cmds.createNode ('multDoubleLinear' , name = 'mult_' + ik_chain_crv)
        cmds.connectAttr (add_curveInfo_node + '.output' , mult_curveInfo_node + '.input1')
        cmds.setAttr (mult_curveInfo_node + '.input2' , 0.25)

        # 给控制器创建一个拉伸的属性，动画师根据需要可以选择是否拉伸
        cmds.addAttr (endIK_ctrl , longName = 'stretch' , attributeType = 'double' ,
                      niceName = u'拉伸' , minValue = 0 , maxValue = 1 , defaultValue = 0 , keyable = 1)

        # 根据对应的关节创建对应的相加节点，将变换后的数值连接到对应的关节上
        for jnt in ik_chain [1 :-1] :
            add_node = cmds.createNode ('addDoubleLinear' , name = 'add_' + jnt)
            cmds.connectAttr (mult_curveInfo_node + '.output' , add_node + '.input1')
            cmds.setAttr (add_node + '.input2' , cmds.getAttr (jnt + '.translateX'))
            # 创建blendcolor节点用来承载拉伸的设置
            blend_node = cmds.createNode ('blendColors' , name = 'blend_' + jnt)
            cmds.connectAttr (endIK_ctrl + '.stretch' , blend_node + '.blender')
            # 设置blendcolor节点混合值为0的时候，也就是没有拉伸的时候，color2R 的值是原关节的长度
            cmds.setAttr (blend_node + '.color2R' , cmds.getAttr (jnt + '.translateX'))
            # 连接拉伸后的关节长度
            cmds.connectAttr (add_node + '.output' , blend_node + '.color1R')
            # 把混合后的关节长度连接给原关节
            cmds.connectAttr (blend_node + '.outputR' , jnt + '.translateX')


    # 删除ik控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def delete_ik_ctrl (objects) :
        for object in objects :
            grp_name = 'grpIKspine_{}'.format (object)
            try :
                cmds.delete (grp_name)
                cmds.warning ('已经删除了{}的ik链条'.format (objects))
            except :
                # 已经被删除的情况就返回
                return


    # 获取参数值
    @staticmethod
    def get_arg (args) :
        if len (args) > 0 :
            return args [0]
        return None


    # 获取控制器形状节点的曲线点位置信息
    @staticmethod
    def get_curve_shape_points (shape) :
        return pm.xform (shape.cv , q = 1 , t = 1)


    # 返回软选择的范围
    @staticmethod
    def get_soft_radius () :
        u"""
        ssd (float): 衰减半径
        return:返回软选择的范围
        """
        return pm.softSelect (query = 1 , ssd = 1)


    # 获取两点之间的距离
    @staticmethod
    def get_length (point1 , point2) :
        u"""
        point1[float,float,float]: 点1的坐标(x,y,z)
        point2[float,float,float]: 点2的坐标(x,y,z)
        return: 两点之间的距离
        原理：两点之间的距离等于两点之间x，y，z相减的和的平方再开方
        ((x1-x2)**2 +(y1-y2)**2 + (z1-z2)**2)**0.5
        ** 表示平方，**0.5表示开方
        """
        distance = sum ([(point1 [i] - point2 [i]) ** 2 for i in range (3)]) ** 0.5
        return distance


    # 获取选择的控制器
    @classmethod
    def selected (cls) :
        u"""
         [Control(), ]
        选择的控制器
        """
        return [cls (t = t) for t in pm.selected (type = "transform")]


    # 批量修改选择的控制器
    @classmethod
    def set_selected (cls , **kwargs) :
        u"""
        :param kwargs: 修改控制器的参数
        批量修改选择的控制器
        """
        selected = cls.selected ()
        for control in selected :
            control.set (**kwargs)
        pm.select ([control.get_transform () for control in selected])


    # 镜像两个选择的控制器
    @classmethod
    def mirror_selected (cls) :
        u"""
        镜像两个选择的控制器
        :return:
        """
        selected = cls.selected ()
        if not len (selected) == 2 :
            return
        src , dst = selected
        src.mirror (dst)


    # 删除形状
    @classmethod
    def delete_shape (cls , *args , **kwargs) :
        """
        删除形状
        :return:
        """
        s = kwargs.get ("s" , kwargs.get ("shape" , cls.get_arg (args)))
        if s is None :
            return
        json_path = os.path.abspath (__file__ + "/../../tools/image/{s}.json".format (s = s))
        if os.path.isfile (json_path) :
            os.remove (json_path)
        jpg_path = os.path.abspath (__file__ + "/../../tools/image/{s}.jpg".format (s = s))
        if os.path.isfile (jpg_path) :
            os.remove (jpg_path)


    # 批量删除形状
    @classmethod
    def delete_shapes (cls , *args) :
        """
        批量删除形状
        :return:
        """
        for s in args :
            cls.delete_shape (s)


    # 创建ribbon控制器
    @staticmethod
    def create_ribbon (name , control_parent , jnt_number = 5) :
        """
        创建ribbon控制器，给动画师更细致的动画效果
        思路：通过给定关节的名称来创建ribbon控制，通过曲线来生成曲面制作ribbon绑定，然后让生成的关节绑定在曲面上
        采用的变形器有twist，sine和wire变形器，通过这些变形器影响曲面，从而带动曲面上的关节

        Args:
            ribbon.side (str): ribbon's ribbon.side
            ribbon.description (str): ribbon's ribbon.description
            ribbon.index (int): ribbon's ribbon.index
            jnt_number (int): how many joints need to be attached to the ribbon, default is 9
            control_parent:

        """
        # 从名称中获取ribbon控制器的边，描述，和编号
        ribbon = nameUtils.Name (name = name)

        # 从ribbon控制器中的边获取偏移值
        if ribbon.side != 'r' :
            offset_val = 1
        else :
            offset_val = -1

        # 创建ribbon控制器对应的层级组
        ribbon_grp = cmds.createNode ('transform' ,
                                      name = 'grp_{}_{}Ribbon_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                              ribbon.index))
        ribbon_ctrl_grp = cmds.createNode ('transform' ,
                                           name = 'grp_{}_{}RibbonCtrls_{:03d}'.format (ribbon.side ,
                                                                                        ribbon.description ,
                                                                                        ribbon.index) ,
                                           parent = ribbon_grp)
        ribbon_jnt_grp = cmds.createNode ('transform' ,
                                          name = 'grp_{}_{}RibbonJnts_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                                      ribbon.index) ,
                                          parent = ribbon_grp)
        nodes_local_grp = cmds.createNode ('transform' ,
                                           name = 'grp_{}_{}RibbonNodesLocal_{:03d}'.format (ribbon.side ,
                                                                                             ribbon.description ,
                                                                                             ribbon.index) ,
                                           parent = ribbon_grp)
        nodes_world_grp = cmds.createNode ('transform' ,
                                           name = 'grp_{}_{}RibbonNodesWorld_{:03d}'.format (ribbon.side ,
                                                                                             ribbon.description ,
                                                                                             ribbon.index) ,
                                           parent = ribbon_grp)
        cmds.setAttr (nodes_world_grp + '.inheritsTransform' , 0)

        cmds.setAttr (nodes_local_grp + '.visibility' , 0)
        cmds.setAttr (nodes_world_grp + '.visibility' , 0)

        # 创建对应的曲线以生成nurbs曲面
        temp_curve = cmds.curve (point = [[-5 * offset_val , 0 , 0] , [5 * offset_val , 0 , 0]] , knot = [0 , 1] ,
                                 degree = 1)
        # 根据关节数重建曲线
        cmds.rebuildCurve (temp_curve , degree = 3 , replaceOriginal = True , rebuildType = 0 , endKnots = 1 ,
                           keepRange = 0 ,
                           keepControlPoints = False , keepEndPoints = True , keepTangents = False ,
                           spans = jnt_number + 1)
        # 复制这条曲线
        temp_curve_02 = cmds.duplicate (temp_curve) [0]
        # 移动两条曲线的位置来制作曲面
        cmds.setAttr (temp_curve + '.translateZ' , 1)
        cmds.setAttr (temp_curve_02 + '.translateZ' , -1)

        # 通过两条曲线来放样制作曲面
        surf = \
            cmds.loft (temp_curve_02 , temp_curve , constructionHistory = False , uniform = True , degree = 3 ,
                       sectionSpans = 1 ,
                       range = False , polygon = 0 ,
                       name = 'surf_{}_{}Ribbon_{:03d}'.format (ribbon.side , ribbon.description , ribbon.index)) [0]
        cmds.parent (surf , nodes_local_grp)

        # 获得曲面的形状节点
        surf_shape = cmds.listRelatives (surf , shapes = True) [0]

        # 删除用来放样曲面的曲线
        cmds.delete (temp_curve , temp_curve_02)

        # 创建关节并附着到曲面
        fol_grp = cmds.createNode ('transform' ,
                                   name = 'grp_{}_{}RibbonFollicles_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                                    ribbon.index) ,
                                   parent = nodes_world_grp)

        # 创建ribbon关节的集合
        ribbon_jnt_set = 'set_ribbonJnt'
        make_ribbon_jnt_set = 'set_' + ribbon.side + '_' + ribbon.description + 'Jnt'
        make_ribbon_jnt_set = cmds.sets (name = make_ribbon_jnt_set , empty = True)
        if not cmds.objExists (ribbon_jnt_set) or cmds.nodeType (ribbon_jnt_set) != 'objectSet' :
            ribbon_jnt_set = cmds.sets (name = ribbon_jnt_set , empty = True)
            cmds.sets (make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)
        else :
            cmds.sets (make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)

        for i in range (jnt_number) :
            # 创建毛囊
            fol_shape = cmds.createNode ('follicle' , name = 'fol_{}_{}Ribbon{:03d}_{:03d}Shape'.format (ribbon.side ,
                                                                                                         ribbon.description ,
                                                                                                         i + 1 ,
                                                                                                         ribbon.index))
            # 重命名毛囊的tran节点名称
            fol = cmds.listRelatives (fol_shape , parent = True) [0]
            fol = cmds.rename (fol , fol_shape [:-5])
            # 把毛囊放入对应的层级组
            cmds.parent (fol , fol_grp)
            # 连接毛囊属性
            cmds.connectAttr (surf_shape + '.worldSpace[0]' , fol_shape + '.inputSurface')
            # 连接毛囊的形状节点以进行变换
            cmds.connectAttr (fol_shape + '.outTranslate' , fol + '.translate')
            cmds.connectAttr (fol_shape + '.outRotate' , fol + '.rotate')
            # 设置uv值
            cmds.setAttr (fol_shape + '.parameterU' , 0.5)
            cmds.setAttr (fol_shape + '.parameterV' , float (i) / (jnt_number - 1))

            # 创建关节
            jnt = cmds.createNode ('joint' ,
                                   name = 'jnt_{}_{}Ribbon{:03d}_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                                 i + 1 ,
                                                                                 ribbon.index))
            parent_grp = ribbon_jnt_grp
            grp_nodes = []
            for node_type in ['zero' , 'offset'] :
                grp = cmds.createNode ('transform' , name = jnt.replace ('jnt' , node_type) , parent = parent_grp)
                grp_nodes.append (grp)
                parent_grp = grp

            cmds.parent (jnt , grp_nodes [-1])
            # 让对应的毛囊约束对应的关节点
            cmds.parentConstraint (fol , grp_nodes [0] , maintainOffset = False)
            # 将偏移组的旋转设置为零
            cmds.xform (grp_nodes [1] , rotation = [0 , 0 , 0] , worldSpace = True)

            # 将生成的ribbon关节放在对应的集里方便选择
            cmds.sets (jnt , edit = True , forceElement = make_ribbon_jnt_set)

        # 创建控制器
        ctrls = []
        for pos in ['start' , 'mid' , 'end'] :
            ctrl_name = 'ctrl_{}_{}{}_{:03d}'.format (ribbon.side , ribbon.description , pos.title () , ribbon.index)
            ctrl = Control.create_ctrl (ctrl_name , shape = 'hexagon' , radius = 5 ,
                                        axis = 'Z+' ,
                                        pos = jnt , parent = ribbon_ctrl_grp)

            ctrls.append (ctrl_name)
        # 放置控制器
        cmds.setAttr (ctrls [0].replace ('ctrl' , 'zero') + '.translateX' , -5 * offset_val)
        cmds.setAttr (ctrls [1].replace ('ctrl' , 'zero') + '.translateX' , 5 * offset_val)

        # 约束中间的控制器
        cmds.pointConstraint (ctrls [0] , ctrls [-1] , ctrls [1].replace ('ctrl' , 'driven') , maintainOffset = False)

        # 添加twist的控制属性在第一个控制器和最后一个控制器上,'start'和 'end'
        cmds.addAttr (ctrls [0] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
        cmds.addAttr (ctrls [-1] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
        # 创建twist变形器
        twist_node , twist_hnd = cmds.nonLinear (surf , type = 'twist' , name = surf.replace ('surf_' , 'twist_'))
        cmds.parent (twist_hnd , nodes_local_grp)
        cmds.setAttr (twist_hnd + '.rotate' , 0 , 0 , 90)
        scale_val = cmds.getAttr (twist_hnd + '.scaleX')
        cmds.setAttr (twist_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
        # 连接twist变形器的属性到控制器上
        twist_hnd_shape = cmds.listRelatives (twist_hnd , shapes = True) [0]
        cmds.connectAttr (ctrls [0] + '.twist' , twist_node + '.endAngle')
        cmds.connectAttr (ctrls [-1] + '.twist' , twist_node + '.startAngle')

        # 添加sine的控制属性在中间的控制器上,'mid'
        cmds.addAttr (ctrls [1] , longName = 'sineDivider' , niceName = u'sine变形器属性设置 ----------' ,
                      attributeType = 'enum' ,
                      enumName = ' ' , keyable = False)
        cmds.setAttr (ctrls [1] + '.sineDivider' , channelBox = True , lock = True)
        cmds.addAttr (ctrls [1] , longName = 'amplitude' , niceName = u'振幅' , attributeType = 'float' ,
                      keyable = True ,
                      minValue = 0)
        cmds.addAttr (ctrls [1] , longName = 'wavelength' , niceName = u'波长' , attributeType = 'float' ,
                      keyable = True ,
                      minValue = 0.1 ,
                      defaultValue = 2)
        cmds.addAttr (ctrls [1] , longName = 'offset' , niceName = u'偏移' , attributeType = 'float' , keyable = True)
        cmds.addAttr (ctrls [1] , longName = 'sineRotation' , niceName = u'正弦旋转' , attributeType = 'float' ,
                      keyable = True)
        # 创建sine变形器
        sine_node , sine_hnd = cmds.nonLinear (surf , type = 'sine' , name = surf.replace ('surf_' , 'sine_'))
        cmds.parent (sine_hnd , nodes_local_grp)
        cmds.setAttr (sine_hnd + '.rotate' , 0 , 0 , 90)
        scale_val = cmds.getAttr (sine_hnd + '.scaleX')
        cmds.setAttr (sine_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
        cmds.setAttr (sine_node + '.dropoff' , 1)
        # 连接sine变形器的属性到控制器上
        sine_hnd_shape = cmds.listRelatives (sine_hnd , shapes = True) [0]
        cmds.connectAttr (ctrls [1] + '.amplitude' , sine_node + '.amplitude')
        cmds.connectAttr (ctrls [1] + '.wavelength' , sine_node + '.wavelength')
        cmds.connectAttr (ctrls [1] + '.offset' , sine_node + '.offset')
        cmds.connectAttr (ctrls [1] + '.sineRotation' , sine_hnd + '.rotateY')

        # 创建wire变形器
        # 创建wire变形器需要的曲线
        wire_curve = cmds.curve (point = [[-5 * offset_val , 0 , 0] , [0 , 0 , 0] , [5 * offset_val , 0 , 0]] ,
                                 knot = [0 , 0 , 1 , 1] ,
                                 degree = 2 ,
                                 name = 'crv_{}_{}RibbonWire_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                             ribbon.index))
        wire_curve_shape = cmds.listRelatives (wire_curve , shapes = True) [0]
        cmds.rename (wire_curve_shape , wire_curve + 'Shape')
        cmds.parent (wire_curve , nodes_world_grp)

        # 创建cluster 变形器，用控制器来约束cluster变形器的变化
        for ctrl , i in zip (ctrls , [0 , 1 , 2]) :
            cls_node , cls_hnd = cmds.cluster ('{}.cv[{}]'.format (wire_curve , i) ,
                                               name = ctrl.replace ('ctrl' , 'cls'))
            cmds.parent (cls_hnd , nodes_world_grp)
            cmds.pointConstraint (ctrl , cls_hnd , maintainOffset = False)

        # 创建wire变形器
        wire_node = surf.replace ('surf' , 'wire')
        cmds.wire (surf , wire = wire_curve , name = wire_node)
        cmds.setAttr (wire_node + '.dropoffDistance[0]' , 200)
        cmds.parent (wire_curve + 'BaseWire' , nodes_local_grp)

        # control = 'control'
        # joint = 'joint'
        # rigNode_Local = 'rigNode_Local'
        # rigNode_World = 'rigNode_World'
        cmds.parent (ribbon_ctrl_grp , control_parent)
        # cmds.parent(ribbon_jnt_grp, joint)
        # cmds.parent(nodes_local_grp, rigNode_Local)
        # cmds.parent(nodes_world_grp, rigNode_World)
        # cmds.delete(ribbon_grp)

        return ribbon_grp , ribbon_ctrl_grp , ribbon_jnt_grp , nodes_local_grp , nodes_world_grp


    def set_control_orientation (self , axis) :
        axis_mapping = {'X+' : (90 , 0 , 0) , 'X-' : (-90 , 0 , 0) , 'Y+' : (0 , 90 , 0) , 'Y-' : (0 , -90 , 0) ,
                        'Z+' : (0 , 0 , 90) , 'Z-' : (0 , 0 , -90)}
        if axis in axis_mapping :
            self.set_rotateX (rx = axis_mapping [axis] [0])
            self.set_rotateY (ry = axis_mapping [axis] [1])
            self.set_rotateZ (rz = axis_mapping [axis] [2])


    @pipelineUtils.Pipeline.make_undo
    def _create_ctrl (self , name , shape , radius , axis , pos , parent = None) :
        u"""基于参数ctrl_side_name_index快速创建控制器

        Args:
            name(str/None): 控制器的名称.
            # side (str/None): 控制器的边.
            # description (str): 控制器的描述.
            # index (int/None): 控制器的编号.
            shape (str): 控制器的形状.
            radius(float):控制器形状的大小.
            pos(str) : 被吸附物体的位置
            axis (str): 控制器的朝向. 'X+'/'X-'/'Y+'/'Y-'/'Z+'/'Z-'
            lock_attrs (list): 要锁定的控制器属性.
            parent (str/None): 控制器的父层级.
            animation_set (str/None): 动画控制器集.



        Raises:
            ValueError: 如果控制器名称已存在.

        Returns:
            ctrl_transform（str）: 控制器的名称

        """
        # 拆分控制器的名称
        name_obj = nameUtils.Name (name = name)
        name_obj.decompose ()

        # 判断需要创建的控制器是否在场景里已经存在，如果存在的话则报错返回
        if cmds.objExists (name_obj.name) :
            raise ValueError (u'{} 在场景中已存在'.format (name_obj.name))

        # 根据控制器边的参数来获取默认控制器的颜色设置
        ctrl_color , sub_color = self.COLORS.get (name_obj.side.lower () , (0 , 0))

        # 创建控制器
        self.ctrl = Control (n = name_obj.name , s = shape , r = radius)
        self.ctrl_transform = self.ctrl.get_transform ()

        # 创建次级控制器
        sub_obj = nameUtils.Name (name = name)
        sub_obj.description = sub_obj.description + 'Sub'
        self.sub_ctrl = Control (n = sub_obj.name , s = shape , r = radius)
        self.sub_ctrl_transform = self.sub_ctrl.get_transform ()

        # 设置控制器的形状方向
        self.ctrl.set_control_orientation (axis)
        self.sub_ctrl.set_control_orientation (axis)

        # 设置控制器的颜色
        self.ctrl.set_color (ctrl_color)
        self.sub_ctrl.set_color (sub_color)

        # 添加上层层级组
        self.offset_grp = hierarchyUtils.Hierarchy.add_extra_group (
            obj = self.ctrl_transform , grp_name = '{}_offset'.format (name) ,
            world_orient = False
        )
        self.connect_grp = hierarchyUtils.Hierarchy.add_extra_group (
            obj = self.offset_grp , grp_name = '{}_connect'.format (self.offset_grp) ,
            world_orient = False
        )
        self.space_grp = hierarchyUtils.Hierarchy.add_extra_group (
            obj = self.connect_grp , grp_name = '{}_space'.format (self.offset_grp) ,
            world_orient = False
        )
        self.driven_grp = hierarchyUtils.Hierarchy.add_extra_group (
            obj = self.space_grp , grp_name = '{}_driven'.format (self.connect_grp) ,
            world_orient = False
        )
        self.zero_grp = hierarchyUtils.Hierarchy.add_extra_group (
            obj = self.driven_grp , grp_name = '{}_zero'.format (self.driven_grp) ,
            world_orient = False
        )

        # 创建output层级组
        self.output_grp = cmds.createNode ('transform' , name = name.replace ('ctrl' , 'output') ,
                                           parent = self.ctrl_transform)

        # 连接次级控制器的属性
        attrs_to_connect = ['.translate' , '.rotate' , '.scale' , '.rotateOrder']
        for attr in attrs_to_connect :
            source_attr = self.ctrl_transform + attr
            target_attr = self.sub_ctrl_transform + attr
            cmds.connectAttr (source_attr , target_attr)

        # # 添加次级控制器的属性控制在控制器上
        cmds.addAttr (self.ctrl_transform , longName = 'subCtrlVis' , attributeType = 'bool')
        cmds.setAttr (self.ctrl_transform + '.subCtrlVis' , channelBox = True)

        # 连接次级控制器的显示
        cmds.connectAttr (self.ctrl_transform + '.subCtrlVis' , self.sub_ctrl_transform + '.visibility')

        # 锁定并且隐藏不需要的属性
        attrUtils.Attr.lock_and_hide_attrs (obj = self.ctrl_transform , attrs_list = ['rotateOrder'] , lock = False ,
                                            hide = False)

        # 吸附到对应的位置
        if pos :
            cmds.matchTransform (self.zero_grp , pos , position = True , rotation = True , scale = True , piv = True)
        #
        # 做父子层级
        if parent :
            hierarchyUtils.Hierarchy.parent (child_node = self.zero_grp , parent_node = parent)

        # 将控制器添加到选择集里方便进行选择
        pipelineUtils.Pipeline.create_set (ctrl_transform ,
                                           set_name = '{}_{}_ctrl_set'.format (name_obj.side ,
                                                                               name_obj.description) ,
                                           set_parent = 'ctrl_set')

        pipelineUtils.Pipeline.create_set (sub_ctrl.transform ,
                                           set_name = '{}_{}_ctrl_set'.format (name_obj.side ,
                                                                               name_obj.description) ,
                                           set_parent = 'ctrl_set')

        return self.ctrl_transform



