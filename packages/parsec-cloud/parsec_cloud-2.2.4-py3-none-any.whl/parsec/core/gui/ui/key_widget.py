# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/key_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KeyWidget(object):
    def setupUi(self, KeyWidget):
        KeyWidget.setObjectName("KeyWidget")
        KeyWidget.setEnabled(True)
        KeyWidget.resize(572, 45)
        KeyWidget.setMinimumSize(QtCore.QSize(20, 45))
        self.horizontalLayout = QtWidgets.QHBoxLayout(KeyWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_org = QtWidgets.QLabel(KeyWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_org.setFont(font)
        self.label_org.setText("")
        self.label_org.setObjectName("label_org")
        self.horizontalLayout.addWidget(self.label_org)
        self.label_user = QtWidgets.QLabel(KeyWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(False)
        self.label_user.setFont(font)
        self.label_user.setText("")
        self.label_user.setObjectName("label_user")
        self.horizontalLayout.addWidget(self.label_user)
        self.label_device = QtWidgets.QLabel(KeyWidget)
        self.label_device.setMinimumSize(QtCore.QSize(0, 0))
        self.label_device.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_device.setFont(font)
        self.label_device.setText("")
        self.label_device.setScaledContents(True)
        self.label_device.setObjectName("label_device")
        self.horizontalLayout.addWidget(self.label_device)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.export_button = QtWidgets.QPushButton(KeyWidget)
        self.export_button.setMaximumSize(QtCore.QSize(16777215, 32))
        self.export_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.export_button.setObjectName("export_button")
        self.horizontalLayout.addWidget(self.export_button)

        self.retranslateUi(KeyWidget)
        QtCore.QMetaObject.connectSlotsByName(KeyWidget)

    def retranslateUi(self, KeyWidget):
        _translate = QtCore.QCoreApplication.translate
        KeyWidget.setWindowTitle(_translate("KeyWidget", "Form"))
        self.export_button.setToolTip(_translate("KeyWidget", "TEXT_EXPORT_KEY_TOOLTIP"))
        self.export_button.setText(_translate("KeyWidget", "ACTION_EXPORT_KEY"))
