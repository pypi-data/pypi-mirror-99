# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/greet_user_instructions_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GreetUserInstructionsWidget(object):
    def setupUi(self, GreetUserInstructionsWidget):
        GreetUserInstructionsWidget.setObjectName("GreetUserInstructionsWidget")
        GreetUserInstructionsWidget.resize(400, 227)
        self.verticalLayout = QtWidgets.QVBoxLayout(GreetUserInstructionsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(GreetUserInstructionsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_start = QtWidgets.QPushButton(GreetUserInstructionsWidget)
        self.button_start.setObjectName("button_start")
        self.horizontalLayout.addWidget(self.button_start)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GreetUserInstructionsWidget)
        QtCore.QMetaObject.connectSlotsByName(GreetUserInstructionsWidget)

    def retranslateUi(self, GreetUserInstructionsWidget):
        _translate = QtCore.QCoreApplication.translate
        GreetUserInstructionsWidget.setWindowTitle(_translate("GreetUserInstructionsWidget", "Form"))
        self.label.setText(_translate("GreetUserInstructionsWidget", "TEXT_GREET_USER_INSTRUCTIONS"))
        self.button_start.setText(_translate("GreetUserInstructionsWidget", "ACTION_START"))
