# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(821, 512)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logos/images/icons/parsec.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.widget_center = QtWidgets.QWidget(MainWindow)
        self.widget_center.setObjectName("widget_center")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_center)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tab_center = QtWidgets.QTabWidget(self.widget_center)
        self.tab_center.setTabsClosable(True)
        self.tab_center.setMovable(True)
        self.tab_center.setTabBarAutoHide(False)
        self.tab_center.setObjectName("tab_center")
        self.horizontalLayout.addWidget(self.tab_center)
        MainWindow.setCentralWidget(self.widget_center)

        self.retranslateUi(MainWindow)
        self.tab_center.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass
from parsec.core.gui import resources_rc
