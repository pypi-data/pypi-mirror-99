# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/new_version_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewVersionDialog(object):
    def setupUi(self, NewVersionDialog):
        NewVersionDialog.setObjectName("NewVersionDialog")
        NewVersionDialog.resize(447, 230)
        NewVersionDialog.setMinimumSize(QtCore.QSize(0, 230))
        NewVersionDialog.setMaximumSize(QtCore.QSize(16777215, 230))
        NewVersionDialog.setStyleSheet("QLabel\n"
"{\n"
"color: rgb(12, 65, 157);\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"color: white;\n"
"background-color: rgb(38, 142, 212);\n"
"border: 0;\n"
"padding: 3px;\n"
"font-size: 15px;\n"
"font-weight: bold;\n"
"height: 32px;\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"background-color: rgb(20, 122, 192);\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"background-color: rgb(112, 112, 112);\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(NewVersionDialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(NewVersionDialog)
        self.widget.setStyleSheet("QWidget#widget\n"
"{\n"
"border: 2px solid rgb(12, 65, 157);\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(348, 60))
        self.label.setMaximumSize(QtCore.QSize(348, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/images/logos/parsec_vert.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setObjectName("layout")
        self.verticalLayout_2.addLayout(self.layout)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(NewVersionDialog)
        QtCore.QMetaObject.connectSlotsByName(NewVersionDialog)

    def retranslateUi(self, NewVersionDialog):
        _translate = QtCore.QCoreApplication.translate
        NewVersionDialog.setWindowTitle(_translate("NewVersionDialog", "Dialog"))
from parsec.core.gui import resources_rc
