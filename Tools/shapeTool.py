import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import sys


def get_maya_window () :
    u'''
    ��ȡmaya�������ڣ��ж�python�İ汾�ţ��������3�Ļ���ʹ��int
    :return:
    '''
    # c++��ָ������ȡmaya�Ĵ��ڶ���
    pointer = omui.MQtUtil.mainWindow ()
    # �ж�python�İ汾�ţ��������3�Ļ���ʹ��int
    if sys.version_info.major >= 3 :
        return wrapInstance (int (pointer) , QWidget)
    else :
        return wrapInstance (long (pointer) , QWidget)


class shape_Tool (QDialog) :
    """
    ����������״����
    """


    def __init__ (self , parent = get_maya_window ()) :
        super (shape_Tool , self).__init__ (parent)
        # ���ô��ڱ���
        self.setWindowTitle ("shape_Tool")
        self.setMinimumWidth (300)

        # ����С���������ֺ�����
        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()


    def create_widgets (self) :
        # ������ƤȨ��ģ�͵�С����
        self.skin_modle_label = QLabel ("��ƤȨ��ģ��:")
        self.skin_modle_line = QLineEdit ()
        self.skin_modle_line.setReadOnly (True)
        self.skin_modle_btn = QPushButton ('ʰȡ')

        # ��������ģ�͵�С����
        self.bs_modle_label = QLabel ("����ģ��:")
        self.bs_modle_line = QLineEdit ()
        self.bs_modle_line.setReadOnly (True)
        self.bs_modle_btn = QPushButton ('ʰȡ')

        # ����ִ�м��������С����
        self.click_btn = QPushButton ('����������״')


    def create_layouts (self) :
        # ������ƤȨ��ҳ�沼��
        self.skin_modle_layout = QHBoxLayout ()
        self.skin_modle_layout.addWidget (self.skin_modle_label)
        self.skin_modle_layout.addWidget (self.skin_modle_line)
        self.skin_modle_layout.addWidget (self.skin_modle_btn)

        # ��������ҳ�沼��
        self.bs_modle_layout = QHBoxLayout ()
        self.bs_modle_layout.addWidget (self.bs_modle_label)
        self.bs_modle_layout.addWidget (self.bs_modle_line)
        self.bs_modle_layout.addWidget (self.bs_modle_btn)

        # ������ҳ��Ĳ���
        # ���ñ�ǩ����
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addLayout (self.skin_modle_layout)
        self.main_layout.addStretch ()
        self.main_layout.addLayout (self.bs_modle_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.click_btn)


    def create_connections (self) :
        self.skin_modle_btn.clicked.connect (self.clicked_skin_modle_btn)
        self.bs_modle_btn.clicked.connect (self.clicked_bs_modle_btn)
        self.click_btn.clicked.connect(self.clicked_click_btn)

    def clicked_skin_modle_btn (self) :
        # ���ӻ�ȡȨ��ģ�͵İ�ť�Ĳۺ���
        self.skin_modle = cmds.ls (sl = True) [0]
        self.skin_modle_line.setText ('{}'.format(self.skin_modle))


    def clicked_bs_modle_btn (self) :
        # ���ӻ�ȡ����ģ�͵İ�ť�Ĳۺ���
        #���ԭ�е�����������
        self.bs_modle_line.clear()
        #��ѡ�������ģ����ѭ������ӽ�����������
        self.bs_modles = cmds.ls (sl = True)
        for bs_modle in self.bs_modles:
            self.bs_modle_line.insert ('{},'.format (bs_modle))

    def clicked_click_btn(self):
        "���Ӽ���������״�Ĳۺ���"
        self.skin_modle = self.skin_modle_line.text()
        bs_modles_list = self.bs_modle_line.text()

        # �ж���������Ƿ��з��ϵĶ���û�еĻ��򱨴�
        if not self.skin_modle :
            cmds.warning ("δ����Ȩ��ģ�ͣ�������ѡ��Ȩ��ģ�ͼ���")
            return
        if not bs_modles_list :
            cmds.warning ("δ������Ҫ���������ģ�͡�������ѡ������ģ�ͽ��м���")
            return

        self.bs_modles = bs_modles_list.split (',')
        for bs_modle in self.bs_modles :
            invert_shape = cmds.invertShape(self.skin_modle, bs_modle)
            cmds.rename(invert_shape, bs_modle + '_invert_geo')


if __name__ == "__main__" :

    try :
        window.close ()  # �رմ���
        window.deleteLater ()  # ɾ������
    except :
        pass
    window = shape_Tool ()  # ����ʵ��
    window.show ()  # ��ʾ����
