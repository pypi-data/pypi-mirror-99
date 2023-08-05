# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/create_org_device_info_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateOrgDeviceInfoWidget(object):
    def setupUi(self, CreateOrgDeviceInfoWidget):
        CreateOrgDeviceInfoWidget.setObjectName("CreateOrgDeviceInfoWidget")
        CreateOrgDeviceInfoWidget.resize(400, 248)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateOrgDeviceInfoWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_device_name = QtWidgets.QLabel(CreateOrgDeviceInfoWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_device_name.setFont(font)
        self.label_device_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_device_name.setObjectName("label_device_name")
        self.verticalLayout_8.addWidget(self.label_device_name)
        self.line_edit_device = ValidatedLineEdit(CreateOrgDeviceInfoWidget)
        self.line_edit_device.setMinimumSize(QtCore.QSize(0, 0))
        self.line_edit_device.setPlaceholderText("")
        self.line_edit_device.setObjectName("line_edit_device")
        self.verticalLayout_8.addWidget(self.line_edit_device)
        self.verticalLayout.addLayout(self.verticalLayout_8)
        self.widget_password = PasswordChoiceWidget(CreateOrgDeviceInfoWidget)
        self.widget_password.setObjectName("widget_password")
        self.verticalLayout.addWidget(self.widget_password)
        spacerItem = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(CreateOrgDeviceInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateOrgDeviceInfoWidget)

    def retranslateUi(self, CreateOrgDeviceInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateOrgDeviceInfoWidget.setWindowTitle(_translate("CreateOrgDeviceInfoWidget", "Form"))
        self.label_device_name.setText(_translate("CreateOrgDeviceInfoWidget", "TEXT_LABEL_DEVICE_NAME"))
from parsec.core.gui.input_widgets import ValidatedLineEdit
from parsec.core.gui.password_validation import PasswordChoiceWidget
