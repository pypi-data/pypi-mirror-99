# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/claim_device_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClaimDeviceWidget(object):
    def setupUi(self, ClaimDeviceWidget):
        ClaimDeviceWidget.setObjectName("ClaimDeviceWidget")
        ClaimDeviceWidget.resize(600, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClaimDeviceWidget.sizePolicy().hasHeightForWidth())
        ClaimDeviceWidget.setSizePolicy(sizePolicy)
        ClaimDeviceWidget.setMinimumSize(QtCore.QSize(0, 0))
        ClaimDeviceWidget.setStyleSheet("#label_device_name, #label_token, #label_password, #label_confirmation {\n"
"    color: #999999;\n"
"    padding-left: 10px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(ClaimDeviceWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget = QtWidgets.QWidget(ClaimDeviceWidget)
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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_layout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.main_layout)
        self.horizontalLayout_3.addWidget(self.widget)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(ClaimDeviceWidget)
        QtCore.QMetaObject.connectSlotsByName(ClaimDeviceWidget)

    def retranslateUi(self, ClaimDeviceWidget):
        _translate = QtCore.QCoreApplication.translate
        ClaimDeviceWidget.setWindowTitle(_translate("ClaimDeviceWidget", "Form"))
