# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/devices_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DevicesWidget(object):
    def setupUi(self, DevicesWidget):
        DevicesWidget.setObjectName("DevicesWidget")
        DevicesWidget.resize(467, 376)
        DevicesWidget.setStyleSheet("#button_add_device {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #0092FF;\n"
"}\n"
"\n"
"#button_add_device:hover {\n"
"    color: #0070DD;\n"
"}\n"
"\n"
"#scrollAreaWidgetContents {\n"
"    background-color: #EEEEEE;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(DevicesWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_add_device = Button(DevicesWidget)
        self.button_add_device.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/add_to_queue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_device.setIcon(icon)
        self.button_add_device.setIconSize(QtCore.QSize(24, 24))
        self.button_add_device.setFlat(True)
        self.button_add_device.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_add_device.setObjectName("button_add_device")
        self.horizontalLayout.addWidget(self.button_add_device)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(DevicesWidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 465, 338))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout_3.addLayout(self.layout_content)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinner = SpinnerWidget(self.scrollAreaWidgetContents)
        self.spinner.setObjectName("spinner")
        self.horizontalLayout_2.addWidget(self.spinner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(DevicesWidget)
        QtCore.QMetaObject.connectSlotsByName(DevicesWidget)

    def retranslateUi(self, DevicesWidget):
        _translate = QtCore.QCoreApplication.translate
        DevicesWidget.setWindowTitle(_translate("DevicesWidget", "Form"))
        self.button_add_device.setToolTip(_translate("DevicesWidget", "TEXT_DEVICE_ADD_NEW_TOOLTIP"))
        self.button_add_device.setText(_translate("DevicesWidget", "ACTION_DEVICE_ADD_NEW"))
from parsec.core.gui.custom_widgets import Button, SpinnerWidget
from parsec.core.gui import resources_rc
