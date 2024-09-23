# coding:utf-8
import os
import json
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


import pymel.core as pm
import selection
import actions
import control
import build
import explorer


ROOT = os.path.abspath(os.path.join(__file__+"../.."))


def update_background():

    for hud in pm.headsUpDisplay( 'HUDObjectPosition', lh=1):
        pm.headsUpDisplay(hud, e=1, vis=False)
    path = os.path.join(ROOT, "ui",  "background")
    file_name = pm.playblast(f=path, fp=0, fmt="image", c="jpg", st=0, et=0, orn=1,
                             os=True, qlt=100, p=100, wh=(512, 640), v=0)
    if os.path.isfile(file_name.replace("####", "0")):
        if os.path.isfile(file_name.replace("####.", "")):
            os.remove(file_name.replace("####.", ""))
        os.rename(file_name.replace("####", "0"), file_name.replace("####.", ""))


def update_buttons():
    data = {}
    camera, err = actions.find_node_by_name("front")
    cp = [0, camera.ty.get(), 0]

    for attr, fun in selection.__dict__.items():
        if "Selection" not in attr:
            continue
        selection_node, err = actions.find_node_by_name(attr, False)
        if err:
            continue
        if selection_node.type() == "joint":
            p = list(selection_node.getTranslation(space="world"))
            points = [[xyz1+xyz2*0.15 for xyz1, xyz2 in zip(p, p1)]
                      for p1 in [[0, 1, 0], [1, 0, 0], [0, -1, 0], [-1, 0, 0], [0, 1, 0]]]

        else:
            points = control.get_curve_shape_points(selection_node.getShape())
        points = [[(xyz1-xyz2)/20 for xyz1, xyz2 in zip(p, cp)][:2] for p in points]
        for wh in points:
            wh[0] = (wh[0] + 0.5) * 512
            wh[1] = (0.625 - wh[1]) * 512
        whs = [[points[i], [0.5*wh1+0.5*wh2 for wh1, wh2 in zip(points[i], point)]]
               for i, point in enumerate(points[1:])]
        whs = sum(whs, [])
        whs.append(points[-1])
        data[attr] = whs
    path = os.path.join(ROOT, "ui", "buttons.json")
    with open(path, "w") as fp:
        json.dump(data, fp, indent=4)


def get_host_app():
    try:
        main_window = QApplication.activeWindow()
        while True:
            last_win = main_window.parent()
            if last_win:
                main_window = last_win
            else:
                break
        return main_window
    except:
        pass


class IconButton(QWidget):
    clicked = Signal()

    def __init__(self, parent, icon):
        QWidget.__init__(self, parent)
        self.icon = QIcon(icon)
        self.mode = QIcon.Disabled
        self.setFixedSize(36, 32)

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)
        if self.width() != self.height():
            self.setMinimumWidth(self.height())
            self.resize(self.height(), self.height())

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.icon.pixmap(self.width(), self.height(), self.mode))
        painter.end()

    def mousePressEvent(self, event):
        if self.mode == QIcon.Disabled:
            return
        self.mode = QIcon.Selected
        self.update()

    def mouseReleaseEvent(self, event):
        if self.mode == QIcon.Disabled:
            return
        self.mode = QIcon.Normal
        self.clicked.emit()
        self.update()


class FaceSelection(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setFixedSize(512, 640)
        self.pix = QPixmap(os.path.join(ROOT, "ui",  "background.jpg"))
        self.build = IconButton(self, os.path.join(ROOT, "ui",  "build.png"))
        self.build.move(512-64, 32)
        path = os.path.join(ROOT, "ui", "buttons.json")
        with open(path, "r") as fp:
            self.data = json.load(fp)
        self.name = None
        self.setMouseTracking(True)
        self.assert_build()
        self.build.clicked.connect(build.build)

    def assert_build(self):
        if all([pm.objExists(attr) for attr in self.data]):
            self.build.mode = QIcon.Normal
        else:
            self.build.mode = QIcon.Disabled

    def paintEvent(self, event):
        QDialog.paintEvent(self, event)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.pix)
        for n, points in self.data.items():
            painter.setPen(QPen(QColor(0, 225, 225), 2, Qt.SolidLine))
            if pm.objExists(n):
                painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
            if self.name == n:
                painter.setPen(QPen(QColor(225, 0, 0), 2, Qt.SolidLine))
            painter.drawLines([QLineF(QPointF(*point), QPointF(*points[i]))
                               for i, point in enumerate(points[1:])])
        painter.end()

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        pos = event.pos()
        for n, points in self.data.items():
            for p in points:
                length = ((p[0] - pos.x()) ** 2 + (p[1] - pos.y()) ** 2)**0.5
                if length < 6:
                    if self.name != n:
                        self.name = n
                        self.update()
                    return
        if not (self.name is None):
            self.name = None
            self.update()

    def mousePressEvent(self, *args, **kwargs):
        if self.name is None:
            return
        if hasattr(selection, self.name):
            getattr(selection, self.name)()
        self.assert_build()
        self.update()

window = None


qss = u"""
QWidget{
    font-size: 14px;
    font-family: 楷体;
} 
"""


class FaceMain(QDialog):
    def __init__(self):
        QDialog.__init__(self, get_host_app())
        self.setStyleSheet(qss)
        self.setWindowTitle("Face")
        layout = QHBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(layout)

        menu_bar = QMenuBar()
        layout.setMenuBar(menu_bar)
        tool = menu_bar.addMenu(u"工具")
        tool.addAction(u"更新次级", actions.update_second)
        tool.addAction(u"控制器显示", actions.update_second)
        tool.addAction(u"眼皮放样", actions.loft_eyelid)
        tool.addAction(u"使用说明", explorer.help)
        tool.addAction(u"开发教程", explorer.study)
        face = FaceSelection()
        layout.addWidget(face)

weight_window = None


def show():
    global window
    if window is None:
        window = FaceMain()
    window.show()
