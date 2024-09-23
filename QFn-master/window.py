# coding:utf-8
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide import QtUiTools
except:
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2 import QtUiTools

import sys
import inspect
import traceback
import data
import args


class Function(object):
    def __init__(self, fn):
        if isinstance(fn, (str, unicode)):
            splits = fn.split(".")
            module_name = ".".join(splits[:-1])
            __import__(module_name)
            self.fn = getattr(sys.modules[module_name], splits[-1])
        elif isinstance(fn, Function):
            self.fn = fn.fn
        else:
            self.fn = fn
        self.name = self.fn.__name__
        self.module = self.fn.__module__
        self.fullName = self.module + "." + self.name
        args_pec = inspect.getargspec(self.fn)
        self.args = args_pec.args
        self.help = self.fn.__doc__
        if args_pec.defaults:
            self.default = dict(zip(args_pec.args[-len(args_pec.defaults)-1:], args_pec.defaults))
        else:
            self.default = {}

    def __call__(self, **kwargs):
        self.fn(**kwargs)

    def __repr__(self):
        return "{self.__module__}.{self.__class__.__name__}('{self.fullName}')".format(self=self)

    def reload(self):
        reload(sys.modules[self.module])
        self.__init__(self.fn)


class FunctionWidget(QFrame):
    def __init__(self, fun):
        QFrame.__init__(self)
        self.function = Function(fun)
        self.setLayout(QFormLayout())
        self.layout().setLabelAlignment(Qt.AlignRight)
        self.menu = QMenu(self)
        self.menu.addAction("reset").triggered.connect(self.reset)
        self.menu.addAction("help").triggered.connect(self.help)
        self.argWidgets = data.AttributeDict()
        for key in self.function.args:
            if key in self.function.default:
                value = self.function.default[key]
                for ArgWidget in args.__all__:
                    label = " ".join([word.capitalize() for word in key.split("_")]) + " : "
                    arg_widget = ArgWidget.instance(value)
                    if arg_widget is not None:
                        self.layout().addRow(label, arg_widget)
                        self.argWidgets[key] = arg_widget
                        break
        if self.layout().count():
            label = self.layout().itemAt(0, self.layout().LabelRole).widget()
            width = QFontMetrics(QFont("System", 14)).width(label.text())
            label.setMinimumWidth(max(162, width))
            label.setAlignment(Qt.AlignRight)
        self.reset()
        self.kwargs = data.argument[self.function.fullName]

    def __repr__(self):
        return "{self.__module__}.{self.__class__.__name__}('{self.function.fullName}')".format(self=self)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    @property
    def kwargs(self):
        return {key: value.arg for key, value in self.argWidgets.items()}

    @kwargs.setter
    def kwargs(self, kwargs):
        for key, value in kwargs.items():
            if key in self.argWidgets:
                self.argWidgets[key].arg = value

    def reset(self):
        self.kwargs = self.function.default

    def help(self):
        QMessageBox.about(self, "help", self.function.help)

    def apply(self):
        try:
            data.argument[self.function.fullName] = self.kwargs
            self.function(**self.kwargs)
        except:
            QMessageBox.about(self, "error", traceback.format_exc())
            self.function.reload()
            raise


class Window(object):
    loader = QtUiTools.QUiLoader()

    def __init__(self, *functions, **kwargs):
        self.functions = functions
        self.name = kwargs.setdefault("name", "lush")
        self.icon = kwargs.setdefault("icon", "lush.jpg")
        self.type = kwargs.setdefault("type", None)
        self._window = None
        if self.type is None:
            if len(self.functions) > 1:
                self.type = "widgets"
            elif Function(self.functions[0]).default:
                self.type = "widget"
            else:
                self.type = "function"

    @property
    def window(self):
        if self._window is None:
            self._window = self.loader.load(data.root + "/window.ui", QDialog(QApplication.activeWindow()))
            self.window.setWindowTitle(self.name)
            self.window.setWindowIcon(QIcon(data.root + "/icons/" + self.icon))
            self.window.apply.clicked.connect(self.apply)
            self.window.setWindowFlags(Qt.WindowFlags(1))
            if self.type == "widget":
                self.window.functionWidget = FunctionWidget(self.functions[0])
                self.window.vlayout.insertWidget(0, self.window.functionWidget)
                self.window.functionWidget.setFrameStyle(
                    self.window.functionWidget.Box | self.window.functionWidget.Raised)
            elif self.type == "widgets":
                self.window.functionTab = QTabWidget()
                self.window.vlayout.insertWidget(0, self.window.functionTab)
                self.window.functionWidgets = data.AttributeDict()
                for fun in self.functions:
                    function_widget = FunctionWidget(fun)
                    label = " ".join([word.capitalize() for word in function_widget.function.name.split("_")])
                    self.window.functionWidgets[function_widget.function.name] = function_widget
                    self.window.functionTab.addTab(function_widget, label)
        return self._window

    def apply(self):
        if self.type == "function":
            Function(self.functions[0])()
        elif self.type == "widget":
            self.window.functionWidget.apply()
        elif self.type == "widgets":
            self.window.functionTab.currentWidget().apply()

    def show(self):
        self.window.show()
