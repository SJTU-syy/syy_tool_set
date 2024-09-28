from __future__ import unicode_literals , print_function

import json
import os.path
import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from importlib import reload
from ..core import pipelineUtils , qtUtils

from . import config, Names_Tool_main, Joint_Tool_main, Rig_Tool_main, Constraint_Tool_main, \
    Connections_Tool_main, Attr_Tool_main, Control_Tool_main, Project_Tool_main

reload (config)
reload (Names_Tool_main)
reload (Joint_Tool_main)
reload (Rig_Tool_main)

reload (Constraint_Tool_main)
reload (Connections_Tool_main)
reload (Attr_Tool_main)
reload (Control_Tool_main)
reload (Project_Tool_main)


class Tool_main_Window(QMainWindow):

    def __init__(self, parent=qtUtils.get_maya_window()):
        super(Tool_main_Window, self).__init__(parent)

        # 设置标题
        self.setWindowTitle("裕焱的工具箱")
        # 设置宽高
        self.setMinimumSize(500, 600)

        # 添加ui布局
        self.add_actions()
        self.add_layouts()

        # 恢复窗口大小和位置和主题设置
        settings = QSettings()
        geometry = settings.value("geometry")
        windowState = settings.value("windowState")
        style_sheet = settings.value("style_sheet")

        # 设置恢复窗口大小
        if geometry is not None:
            self.restoreGeometry(geometry)
        # 设置恢复窗口位置
        if windowState is not None:
            self.restoreState(windowState)

        # 设置恢复qt样式表
        if style_sheet is not None:
            self.setStyleSheet(qtUtils.QSSLoader.read_qss_file(config.qss_dir + './{}.qss'.format(style_sheet)))

    # 创建标签
    def add_actions(self):
        self.close_action = QAction("Close", self)
        self.help_documents_action = QAction("About", self)

        # 主题设置的action
        self.manjaroMix_action = QAction('manjaroMix', self)
        self.amoled_action = QAction('amoled', self)
        self.shared_action = QAction('shared', self)
        self.black_action = QAction('black', self)
        self.lightblack_action = QAction('lightblack', self)
        self.simplicity_action = QAction('simplicity', self)
        self.evilworks_action = QAction('evilworks', self)
        self.liang_style_action = QAction('liang_style', self)
        self.qDarkStyleSheet_action = QAction('qDarkStyleSheet', self)

        self.theme_Actions = [
            self.manjaroMix_action, self.amoled_action, self.shared_action, self.black_action,
            self.lightblack_action, self.simplicity_action, self.evilworks_action,
            self.liang_style_action, self.qDarkStyleSheet_action
        ]

    def add_actions_connect(self):
        """连接actions的信号"""
        self.theme_menu.hovered.connect(self.on_menu_hovered)

    def on_menu_hovered(self, action):
        """
        连接主题菜单的槽函数，在鼠标悬浮上空时发射该信号，获取悬浮位置的action的名称然后更新主题设置
        """
        if isinstance(action, QAction):
            style_sheet = action.text()
            # 保存主题在settings里
            settings = QSettings()
            settings.setValue("style_sheet", style_sheet)
            self.setStyleSheet(qtUtils.QSSLoader.read_qss_file(config.qss_dir + './{}.qss'.format(style_sheet)))

    def add_layouts(self):
        # 创建主窗口的中央小部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建主布局，使用 QVBoxLayout，菜单在上，内容在下
        main_layout = QVBoxLayout(central_widget)

        # 创建菜单区域的布局，使用QVBoxLayout进行垂直排列
        self.menu_layout = QVBoxLayout()
        main_layout.addLayout(self.menu_layout)

        # 创建主内容区域，使用 QStackedWidget
        self.main_content_widget = QStackedWidget()
        main_layout.addWidget(self.main_content_widget)

        # 添加菜单行
        self.add_attr_menu()
        self.add_rig_menu()
        self.add_animation_menu()

    def add_attr_menu(self):
        """添加Attr行的菜单，控制显示Attr相关页面"""
        attr_tab_widget = QTabWidget()

        # 创建Attr和Names页面
        attr_page = Attr_Tool_main.main()
        names_page = Names_Tool_main.main()
        project_page = Project_Tool_main.main()

        # 将页面添加到主内容的StackedWidget中
        self.main_content_widget.addWidget(attr_page)
        self.main_content_widget.addWidget(names_page)
        self.main_content_widget.addWidget(project_page)

        # 添加Tab，点击时切换主内容
        attr_tab_widget.addTab(QWidget(), 'Attr')
        attr_tab_widget.addTab(QWidget(), 'Names')
        attr_tab_widget.addTab(QWidget(), 'Project')

        # 信号连接，点击tab切换主内容页面
        attr_tab_widget.currentChanged.connect(lambda index: self.switch_main_widget(index, [attr_page, names_page, project_page]))

        # 将此行菜单添加到菜单布局中
        self.menu_layout.addWidget(attr_tab_widget)

    def add_rig_menu(self):
        """添加Rig行的菜单，控制显示Rig相关页面"""
        rig_tab_widget = QTabWidget()

        # 创建绑定相关页面
        rig_page = Rig_Tool_main.main()
        constraint_page = Constraint_Tool_main.main()
        joint_page = Joint_Tool_main.main()
        control_page = Control_Tool_main.main()
        connections_page = Connections_Tool_main.main()

        # 将页面添加到主内容的StackedWidget中
        self.main_content_widget.addWidget(rig_page)
        self.main_content_widget.addWidget(constraint_page)
        self.main_content_widget.addWidget(joint_page)
        self.main_content_widget.addWidget(control_page)
        self.main_content_widget.addWidget(connections_page)

        # 添加Tab，点击时切换主内容
        rig_tab_widget.addTab(QWidget(), 'Rig')
        rig_tab_widget.addTab(QWidget(), 'Constraint')
        rig_tab_widget.addTab(QWidget(), 'Joint')
        rig_tab_widget.addTab(QWidget(), 'Control')
        rig_tab_widget.addTab(QWidget(), 'Connections')

        # 信号连接，点击tab切换主内容页面
        rig_tab_widget.currentChanged.connect(
            lambda index: self.switch_main_widget(index, [rig_page, constraint_page, joint_page, control_page, connections_page]))

        # 将此行菜单添加到菜单布局中
        self.menu_layout.addWidget(rig_tab_widget)

    def add_animation_menu(self):
        """添加Animation行的菜单，控制显示Animation相关页面"""
        animation_tab_widget = QTabWidget()

        # 创建动画工具页面
        animation_page = QWidget()  # 占位符，未来可以替换为实际内容

        # 将页面添加到主内容的StackedWidget中
        self.main_content_widget.addWidget(animation_page)

        # 添加Tab，点击时切换主内容
        animation_tab_widget.addTab(QWidget(), 'Animation Tools')

        # 信号连接，点击tab切换主内容页面
        animation_tab_widget.currentChanged.connect(lambda index: self.switch_main_widget(index, [animation_page]))

        # 将此行菜单添加到菜单布局中
        self.menu_layout.addWidget(animation_tab_widget)

    def switch_main_widget(self, index, pages):
        """根据tab切换显示不同的页面"""
        if index < len(pages):
            self.main_content_widget.setCurrentWidget(pages[index])

    def closeEvent (self , event) :
        # 关闭窗口时保存窗口大小和位置,重写了closeEvent方法
        settings = QSettings ()
        settings.setValue ("geometry" , self.saveGeometry ())
        settings.setValue ("windowState" , self.saveState ())
        super ().closeEvent (event)


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Tool_main_Window ()  # 创建实例
    window.show ()  # 显示窗口
