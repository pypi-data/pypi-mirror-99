# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/code_input_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CodeInputWidget(object):
    def setupUi(self, CodeInputWidget):
        CodeInputWidget.setObjectName("CodeInputWidget")
        CodeInputWidget.resize(327, 280)
        self.verticalLayout = QtWidgets.QVBoxLayout(CodeInputWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.code_layout = QtWidgets.QGridLayout()
        self.code_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.code_layout.setSpacing(30)
        self.code_layout.setObjectName("code_layout")
        self.verticalLayout.addLayout(self.code_layout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_none = QtWidgets.QPushButton(CodeInputWidget)
        self.button_none.setMinimumSize(QtCore.QSize(0, 0))
        self.button_none.setObjectName("button_none")
        self.horizontalLayout.addWidget(self.button_none)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CodeInputWidget)
        QtCore.QMetaObject.connectSlotsByName(CodeInputWidget)

    def retranslateUi(self, CodeInputWidget):
        _translate = QtCore.QCoreApplication.translate
        CodeInputWidget.setWindowTitle(_translate("CodeInputWidget", "Form"))
        self.button_none.setText(_translate("CodeInputWidget", "ACTION_CODE_NONE"))
