# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/account_button.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AccountButton(object):
    def setupUi(self, AccountButton):
        AccountButton.setObjectName("AccountButton")
        AccountButton.resize(356, 90)
        AccountButton.setMinimumSize(QtCore.QSize(0, 90))
        AccountButton.setMaximumSize(QtCore.QSize(16777215, 90))
        AccountButton.setStyleSheet("QWidget#AccountButton {\n"
"    border-radius: 8px;\n"
"    background-color: #FFFFFF;\n"
"}\n"
"\n"
"QWidget#widget {\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #CCCCCC;\n"
"}\n"
"\n"
"QWidget#widget:hover {\n"
"    background-color: #F8F8F8;\n"
"    border: 1px solid #999999;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #333333;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(AccountButton)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(AccountButton)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(20, 10, 20, 10)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_organization = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_organization.setFont(font)
        self.label_organization.setText("")
        self.label_organization.setObjectName("label_organization")
        self.verticalLayout_2.addWidget(self.label_organization)
        self.label_name = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_name.setFont(font)
        self.label_name.setText("")
        self.label_name.setObjectName("label_name")
        self.verticalLayout_2.addWidget(self.label_name)
        self.label_device = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_device.setFont(font)
        self.label_device.setText("")
        self.label_device.setObjectName("label_device")
        self.verticalLayout_2.addWidget(self.label_device)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(AccountButton)
        QtCore.QMetaObject.connectSlotsByName(AccountButton)

    def retranslateUi(self, AccountButton):
        _translate = QtCore.QCoreApplication.translate
        AccountButton.setWindowTitle(_translate("AccountButton", "Form"))
