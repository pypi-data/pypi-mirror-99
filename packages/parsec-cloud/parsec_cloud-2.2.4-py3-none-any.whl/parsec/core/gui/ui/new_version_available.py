# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/new_version_available.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewVersionAvailable(object):
    def setupUi(self, NewVersionAvailable):
        NewVersionAvailable.setObjectName("NewVersionAvailable")
        NewVersionAvailable.resize(400, 130)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(NewVersionAvailable)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(NewVersionAvailable)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.button_download = QtWidgets.QPushButton(NewVersionAvailable)
        self.button_download.setMinimumSize(QtCore.QSize(0, 48))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_download.setFont(font)
        self.button_download.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_download.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.button_download.setStyleSheet("")
        self.button_download.setIconSize(QtCore.QSize(30, 30))
        self.button_download.setObjectName("button_download")
        self.horizontalLayout_3.addWidget(self.button_download)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.button_ignore = QtWidgets.QPushButton(NewVersionAvailable)
        self.button_ignore.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_ignore.setFont(font)
        self.button_ignore.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_ignore.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.button_ignore.setStyleSheet("")
        self.button_ignore.setIconSize(QtCore.QSize(20, 20))
        self.button_ignore.setObjectName("button_ignore")
        self.horizontalLayout_2.addWidget(self.button_ignore)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(NewVersionAvailable)
        QtCore.QMetaObject.connectSlotsByName(NewVersionAvailable)

    def retranslateUi(self, NewVersionAvailable):
        _translate = QtCore.QCoreApplication.translate
        NewVersionAvailable.setWindowTitle(_translate("NewVersionAvailable", "Form"))
        self.button_download.setText(_translate("NewVersionAvailable", "ACTION_PARSEC_DOWNLOAD_NEW_VERSION"))
        self.button_ignore.setText(_translate("NewVersionAvailable", "ACTION_PARSEC_IGNORE_NEW_VERSION"))
