# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/password_change_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PasswordChangeWidget(object):
    def setupUi(self, PasswordChangeWidget):
        PasswordChangeWidget.setObjectName("PasswordChangeWidget")
        PasswordChangeWidget.resize(524, 301)
        self.verticalLayout = QtWidgets.QVBoxLayout(PasswordChangeWidget)
        self.verticalLayout.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(PasswordChangeWidget)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(PasswordChangeWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.line_edit_old_password = QtWidgets.QLineEdit(PasswordChangeWidget)
        self.line_edit_old_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_old_password.setObjectName("line_edit_old_password")
        self.verticalLayout_2.addWidget(self.line_edit_old_password)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.label_3 = QtWidgets.QLabel(PasswordChangeWidget)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_new_password = PasswordChoiceWidget(PasswordChangeWidget)
        self.widget_new_password.setObjectName("widget_new_password")
        self.verticalLayout.addWidget(self.widget_new_password)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_change = QtWidgets.QPushButton(PasswordChangeWidget)
        self.button_change.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_change.setObjectName("button_change")
        self.horizontalLayout_2.addWidget(self.button_change)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(PasswordChangeWidget)
        QtCore.QMetaObject.connectSlotsByName(PasswordChangeWidget)

    def retranslateUi(self, PasswordChangeWidget):
        _translate = QtCore.QCoreApplication.translate
        PasswordChangeWidget.setWindowTitle(_translate("PasswordChangeWidget", "Form"))
        self.label.setText(_translate("PasswordChangeWidget", "TEXT_PASSWORD_CHANGE_OLD_PASSWORD_INSTRUCTIONS"))
        self.label_2.setText(_translate("PasswordChangeWidget", "TEXT_LABEL_PASSWORD_OLD"))
        self.label_3.setText(_translate("PasswordChangeWidget", "TEXT_PASSWORD_CHANGE_NEW_PASSWORD_INSTRUCTIONS"))
        self.button_change.setText(_translate("PasswordChangeWidget", "ACTION_CHANGE_PASSWORD"))
from parsec.core.gui.password_validation import PasswordChoiceWidget
