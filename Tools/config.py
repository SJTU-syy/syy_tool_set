from __future__ import unicode_literals
import os
from enum import Enum , unique


#############################################################
# 配置模块
#############################################################


# 路径
project_root = os.path.dirname (__file__)
data_dir = os.path.abspath (__file__ + "/../image")
ui_dir = os.path.abspath (__file__ + "/../ui")
icon_dir = os.path.abspath (__file__ + "/../icon")
qss_dir = os.path.abspath (__file__ + "/../qss")
ma_dir = os.path.abspath (__file__ + "/../ma")
# 是否处于DEBUG状态
DEBUG = True
VERSION = 'v0.1'

# 全局变量
