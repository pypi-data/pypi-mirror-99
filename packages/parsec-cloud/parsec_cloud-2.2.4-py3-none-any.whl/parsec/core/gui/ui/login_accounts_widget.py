# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/login_accounts_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginAccountsWidget(object):
    def setupUi(self, LoginAccountsWidget):
        LoginAccountsWidget.setObjectName("LoginAccountsWidget")
        LoginAccountsWidget.resize(400, 300)
        LoginAccountsWidget.setMinimumSize(QtCore.QSize(0, 300))
        LoginAccountsWidget.setMaximumSize(QtCore.QSize(16777215, 300))
        LoginAccountsWidget.setStyleSheet("#accounts_widget {\n"
"    background-color: #EEEEEE;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginAccountsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(LoginAccountsWidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.accounts_widget = QtWidgets.QWidget()
        self.accounts_widget.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.accounts_widget.setObjectName("accounts_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.accounts_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.scrollArea.setWidget(self.accounts_widget)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(LoginAccountsWidget)
        QtCore.QMetaObject.connectSlotsByName(LoginAccountsWidget)

    def retranslateUi(self, LoginAccountsWidget):
        _translate = QtCore.QCoreApplication.translate
        LoginAccountsWidget.setWindowTitle(_translate("LoginAccountsWidget", "Form"))
