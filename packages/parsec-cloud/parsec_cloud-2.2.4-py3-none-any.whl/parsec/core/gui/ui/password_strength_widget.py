# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/password_strength_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PasswordStrengthWidget(object):
    def setupUi(self, PasswordStrengthWidget):
        PasswordStrengthWidget.setObjectName("PasswordStrengthWidget")
        PasswordStrengthWidget.resize(400, 32)
        PasswordStrengthWidget.setMinimumSize(QtCore.QSize(0, 32))
        PasswordStrengthWidget.setMaximumSize(QtCore.QSize(16777215, 32))
        self.horizontalLayout = QtWidgets.QHBoxLayout(PasswordStrengthWidget)
        self.horizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(PasswordStrengthWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(PasswordStrengthWidget)
        QtCore.QMetaObject.connectSlotsByName(PasswordStrengthWidget)

    def retranslateUi(self, PasswordStrengthWidget):
        _translate = QtCore.QCoreApplication.translate
        PasswordStrengthWidget.setWindowTitle(_translate("PasswordStrengthWidget", "Form"))
