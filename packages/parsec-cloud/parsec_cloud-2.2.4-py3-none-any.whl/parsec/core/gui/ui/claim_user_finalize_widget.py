# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/claim_user_finalize_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClaimUserFinalizeWidget(object):
    def setupUi(self, ClaimUserFinalizeWidget):
        ClaimUserFinalizeWidget.setObjectName("ClaimUserFinalizeWidget")
        ClaimUserFinalizeWidget.resize(400, 240)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClaimUserFinalizeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ClaimUserFinalizeWidget)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.widget_password = PasswordChoiceWidget(ClaimUserFinalizeWidget)
        self.widget_password.setObjectName("widget_password")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_password)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.widget_password)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.button_finalize = QtWidgets.QPushButton(ClaimUserFinalizeWidget)
        self.button_finalize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_finalize.setObjectName("button_finalize")
        self.horizontalLayout.addWidget(self.button_finalize)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ClaimUserFinalizeWidget)
        QtCore.QMetaObject.connectSlotsByName(ClaimUserFinalizeWidget)

    def retranslateUi(self, ClaimUserFinalizeWidget):
        _translate = QtCore.QCoreApplication.translate
        ClaimUserFinalizeWidget.setWindowTitle(_translate("ClaimUserFinalizeWidget", "Form"))
        self.label.setText(_translate("ClaimUserFinalizeWidget", "TEXT_CLAIM_USER_FINALIZE_INSTRUCTIONS"))
        self.button_finalize.setText(_translate("ClaimUserFinalizeWidget", "ACTION_OK"))
from parsec.core.gui.password_validation import PasswordChoiceWidget
