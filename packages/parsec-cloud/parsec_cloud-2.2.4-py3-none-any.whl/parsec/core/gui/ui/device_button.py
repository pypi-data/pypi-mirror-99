# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/device_button.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeviceButton(object):
    def setupUi(self, DeviceButton):
        DeviceButton.setObjectName("DeviceButton")
        DeviceButton.resize(280, 280)
        DeviceButton.setMinimumSize(QtCore.QSize(280, 280))
        DeviceButton.setMaximumSize(QtCore.QSize(280, 280))
        font = QtGui.QFont()
        font.setPointSize(12)
        DeviceButton.setFont(font)
        DeviceButton.setStyleSheet("#DeviceButton, #widget\n"
"{\n"
"background-color: #FFFFFF;\n"
"border-radius: 8px;\n"
"}\n"
"\n"
"#label_is_current\n"
"{\n"
"color: #999999;\n"
"}\n"
"\n"
"#label_device_name\n"
"{\n"
"color: #0092FF;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(DeviceButton)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(DeviceButton)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_icon = IconLabel(self.widget)
        self.label_icon.setMinimumSize(QtCore.QSize(64, 64))
        self.label_icon.setMaximumSize(QtCore.QSize(64, 64))
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap(":/icons/images/material/desktop_windows.svg"))
        self.label_icon.setScaledContents(True)
        self.label_icon.setProperty("color", QtGui.QColor(153, 153, 153))
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout.addWidget(self.label_icon)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_device_name = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_device_name.setFont(font)
        self.label_device_name.setText("")
        self.label_device_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_device_name.setObjectName("label_device_name")
        self.verticalLayout_2.addWidget(self.label_device_name)
        self.label_is_current = QtWidgets.QLabel(self.widget)
        self.label_is_current.setText("")
        self.label_is_current.setAlignment(QtCore.Qt.AlignCenter)
        self.label_is_current.setObjectName("label_is_current")
        self.verticalLayout_2.addWidget(self.label_is_current)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(DeviceButton)
        QtCore.QMetaObject.connectSlotsByName(DeviceButton)

    def retranslateUi(self, DeviceButton):
        _translate = QtCore.QCoreApplication.translate
        DeviceButton.setWindowTitle(_translate("DeviceButton", "Form"))
from parsec.core.gui.custom_widgets import IconLabel
from parsec.core.gui import resources_rc
