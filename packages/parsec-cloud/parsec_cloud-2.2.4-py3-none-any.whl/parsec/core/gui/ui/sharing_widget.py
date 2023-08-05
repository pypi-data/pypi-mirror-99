# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/sharing_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SharingWidget(object):
    def setupUi(self, SharingWidget):
        SharingWidget.setObjectName("SharingWidget")
        SharingWidget.setEnabled(True)
        SharingWidget.resize(572, 45)
        SharingWidget.setMinimumSize(QtCore.QSize(20, 45))
        SharingWidget.setStyleSheet("#SharingWidget:!disabled\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#button_delete\n"
"{\n"
"border: 0;\n"
"background: 0;\n"
"}\n"
"\n"
"#label_email {\n"
"    color: #999999;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(SharingWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 20, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name = QtWidgets.QLabel(SharingWidget)
        self.label_name.setText("")
        self.label_name.setObjectName("label_name")
        self.verticalLayout.addWidget(self.label_name)
        self.label_email = QtWidgets.QLabel(SharingWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_email.setFont(font)
        self.label_email.setText("")
        self.label_email.setObjectName("label_email")
        self.verticalLayout.addWidget(self.label_email)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.combo_role = ComboBox(SharingWidget)
        self.combo_role.setMinimumSize(QtCore.QSize(150, 32))
        self.combo_role.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.combo_role.setFont(font)
        self.combo_role.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.combo_role.setObjectName("combo_role")
        self.horizontalLayout.addWidget(self.combo_role)
        self.label_status = QtWidgets.QLabel(SharingWidget)
        self.label_status.setMinimumSize(QtCore.QSize(24, 24))
        self.label_status.setMaximumSize(QtCore.QSize(24, 24))
        self.label_status.setText("")
        self.label_status.setScaledContents(True)
        self.label_status.setObjectName("label_status")
        self.horizontalLayout.addWidget(self.label_status)

        self.retranslateUi(SharingWidget)
        QtCore.QMetaObject.connectSlotsByName(SharingWidget)

    def retranslateUi(self, SharingWidget):
        _translate = QtCore.QCoreApplication.translate
        SharingWidget.setWindowTitle(_translate("SharingWidget", "Form"))
from parsec.core.gui.custom_widgets import ComboBox
