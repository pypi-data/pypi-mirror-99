# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/new_version_info.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewVersionInfo(object):
    def setupUi(self, NewVersionInfo):
        NewVersionInfo.setObjectName("NewVersionInfo")
        NewVersionInfo.resize(400, 131)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewVersionInfo)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_waiting = QtWidgets.QLabel(NewVersionInfo)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_waiting.setFont(font)
        self.label_waiting.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_waiting.setAlignment(QtCore.Qt.AlignCenter)
        self.label_waiting.setObjectName("label_waiting")
        self.verticalLayout.addWidget(self.label_waiting)
        self.label_error = QtWidgets.QLabel(NewVersionInfo)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_error.setFont(font)
        self.label_error.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error.setObjectName("label_error")
        self.verticalLayout.addWidget(self.label_error)
        self.label_up_to_date = QtWidgets.QLabel(NewVersionInfo)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_up_to_date.setFont(font)
        self.label_up_to_date.setAlignment(QtCore.Qt.AlignCenter)
        self.label_up_to_date.setObjectName("label_up_to_date")
        self.verticalLayout.addWidget(self.label_up_to_date)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.button_close = QtWidgets.QPushButton(NewVersionInfo)
        self.button_close.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_close.setFont(font)
        self.button_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_close.setObjectName("button_close")
        self.horizontalLayout_5.addWidget(self.button_close)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(NewVersionInfo)
        QtCore.QMetaObject.connectSlotsByName(NewVersionInfo)

    def retranslateUi(self, NewVersionInfo):
        _translate = QtCore.QCoreApplication.translate
        NewVersionInfo.setWindowTitle(_translate("NewVersionInfo", "Form"))
        self.label_waiting.setText(_translate("NewVersionInfo", "TEXT_NEW_VERSION_CHECKING_IN_PROGRESS"))
        self.label_error.setText(_translate("NewVersionInfo", "TEXT_NEW_VERSION_CHECK_FAILED"))
        self.label_up_to_date.setText(_translate("NewVersionInfo", "TEXT_NEW_VERSION_UP_TO_DATE"))
        self.button_close.setText(_translate("NewVersionInfo", "ACTION_CLOSE"))
