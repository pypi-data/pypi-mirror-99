# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/claim_device_instructions_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClaimDeviceInstructionsWidget(object):
    def setupUi(self, ClaimDeviceInstructionsWidget):
        ClaimDeviceInstructionsWidget.setObjectName("ClaimDeviceInstructionsWidget")
        ClaimDeviceInstructionsWidget.resize(400, 64)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClaimDeviceInstructionsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ClaimDeviceInstructionsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLineWidth(0)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_start = QtWidgets.QPushButton(ClaimDeviceInstructionsWidget)
        self.button_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_start.setObjectName("button_start")
        self.horizontalLayout.addWidget(self.button_start)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ClaimDeviceInstructionsWidget)
        QtCore.QMetaObject.connectSlotsByName(ClaimDeviceInstructionsWidget)

    def retranslateUi(self, ClaimDeviceInstructionsWidget):
        _translate = QtCore.QCoreApplication.translate
        ClaimDeviceInstructionsWidget.setWindowTitle(_translate("ClaimDeviceInstructionsWidget", "Form"))
        self.label.setText(_translate("ClaimDeviceInstructionsWidget", "TEXT_CLAIM_DEVICE_INSTRUCTIONS"))
        self.button_start.setText(_translate("ClaimDeviceInstructionsWidget", "ACTION_START"))
