# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/claim_device_provide_info_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClaimDeviceProvideInfoWidget(object):
    def setupUi(self, ClaimDeviceProvideInfoWidget):
        ClaimDeviceProvideInfoWidget.setObjectName("ClaimDeviceProvideInfoWidget")
        ClaimDeviceProvideInfoWidget.resize(400, 358)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClaimDeviceProvideInfoWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(ClaimDeviceProvideInfoWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget_info = QtWidgets.QWidget(ClaimDeviceProvideInfoWidget)
        self.widget_info.setObjectName("widget_info")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_info)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_device = QtWidgets.QLabel(self.widget_info)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_device.setFont(font)
        self.label_device.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_device.setObjectName("label_device")
        self.verticalLayout_8.addWidget(self.label_device)
        self.line_edit_device = ValidatedLineEdit(self.widget_info)
        self.line_edit_device.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_device.setFont(font)
        self.line_edit_device.setText("")
        self.line_edit_device.setObjectName("line_edit_device")
        self.verticalLayout_8.addWidget(self.line_edit_device)
        self.verticalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout.addWidget(self.widget_info)
        self.widget_password = PasswordChoiceWidget(ClaimDeviceProvideInfoWidget)
        self.widget_password.setObjectName("widget_password")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_password)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout.addWidget(self.widget_password)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.button_ok = QtWidgets.QPushButton(ClaimDeviceProvideInfoWidget)
        self.button_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_ok.setObjectName("button_ok")
        self.horizontalLayout_3.addWidget(self.button_ok)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_wait = QtWidgets.QLabel(ClaimDeviceProvideInfoWidget)
        self.label_wait.setObjectName("label_wait")
        self.verticalLayout.addWidget(self.label_wait)

        self.retranslateUi(ClaimDeviceProvideInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(ClaimDeviceProvideInfoWidget)

    def retranslateUi(self, ClaimDeviceProvideInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        ClaimDeviceProvideInfoWidget.setWindowTitle(_translate("ClaimDeviceProvideInfoWidget", "Form"))
        self.label_4.setText(_translate("ClaimDeviceProvideInfoWidget", "TEXT_CLAIM_DEVICE_PROVIDE_INFO_INSTRUCTIONS"))
        self.label_device.setText(_translate("ClaimDeviceProvideInfoWidget", "TEXT_LABEL_DEVICE"))
        self.line_edit_device.setPlaceholderText(_translate("ClaimDeviceProvideInfoWidget", "TEXT_LABEL_DEVICE_PLACEHOLDER"))
        self.button_ok.setText(_translate("ClaimDeviceProvideInfoWidget", "ACTION_CREATE_DEVICE"))
        self.label_wait.setText(_translate("ClaimDeviceProvideInfoWidget", "TEXT_CLAIM_DEVICE_WAIT_FOR_DEVICE_INFO"))
from parsec.core.gui.input_widgets import ValidatedLineEdit
from parsec.core.gui.password_validation import PasswordChoiceWidget
