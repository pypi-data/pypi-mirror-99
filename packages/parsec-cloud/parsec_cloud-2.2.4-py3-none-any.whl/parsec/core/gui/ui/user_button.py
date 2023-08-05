# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/user_button.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserButton(object):
    def setupUi(self, UserButton):
        UserButton.setObjectName("UserButton")
        UserButton.resize(280, 280)
        UserButton.setMinimumSize(QtCore.QSize(280, 280))
        UserButton.setMaximumSize(QtCore.QSize(280, 280))
        font = QtGui.QFont()
        font.setPointSize(12)
        UserButton.setFont(font)
        UserButton.setStyleSheet("#label_created_title, #label_role, #label_user_is_current, #label_revoked {\n"
"    color: #999999;\n"
"}\n"
"\n"
"#UserButton, #widget {\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#label_username {\n"
"color: #0092FF;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(UserButton)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(UserButton)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_icon = IconLabel(self.widget)
        self.label_icon.setMinimumSize(QtCore.QSize(64, 64))
        self.label_icon.setMaximumSize(QtCore.QSize(64, 64))
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap(":/icons/images/material/account_circle.svg"))
        self.label_icon.setScaledContents(True)
        self.label_icon.setProperty("color", QtGui.QColor(153, 153, 153))
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout.addWidget(self.label_icon)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_username = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_username.setFont(font)
        self.label_username.setText("")
        self.label_username.setAlignment(QtCore.Qt.AlignCenter)
        self.label_username.setObjectName("label_username")
        self.verticalLayout_2.addWidget(self.label_username)
        self.label_email = QtWidgets.QLabel(self.widget)
        self.label_email.setText("")
        self.label_email.setAlignment(QtCore.Qt.AlignCenter)
        self.label_email.setObjectName("label_email")
        self.verticalLayout_2.addWidget(self.label_email)
        self.label_is_current = QtWidgets.QLabel(self.widget)
        self.label_is_current.setText("")
        self.label_is_current.setAlignment(QtCore.Qt.AlignCenter)
        self.label_is_current.setObjectName("label_is_current")
        self.verticalLayout_2.addWidget(self.label_is_current)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.label_role = QtWidgets.QLabel(self.widget)
        self.label_role.setText("")
        self.label_role.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_role.setObjectName("label_role")
        self.verticalLayout_2.addWidget(self.label_role)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(UserButton)
        QtCore.QMetaObject.connectSlotsByName(UserButton)

    def retranslateUi(self, UserButton):
        _translate = QtCore.QCoreApplication.translate
        UserButton.setWindowTitle(_translate("UserButton", "Form"))
from parsec.core.gui.custom_widgets import IconLabel
from parsec.core.gui import resources_rc
