# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/greet_device_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GreetDeviceWidget(object):
    def setupUi(self, GreetDeviceWidget):
        GreetDeviceWidget.setObjectName("GreetDeviceWidget")
        GreetDeviceWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(GreetDeviceWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget = QtWidgets.QWidget(GreetDeviceWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(350, 200))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.verticalLayout_3.addLayout(self.main_layout)
        self.horizontalLayout_3.addWidget(self.widget)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(GreetDeviceWidget)
        QtCore.QMetaObject.connectSlotsByName(GreetDeviceWidget)

    def retranslateUi(self, GreetDeviceWidget):
        _translate = QtCore.QCoreApplication.translate
        GreetDeviceWidget.setWindowTitle(_translate("GreetDeviceWidget", "Form"))
