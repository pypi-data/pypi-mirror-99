# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/temporary_workspace_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TemporaryWorkspaceWidget(object):
    def setupUi(self, TemporaryWorkspaceWidget):
        TemporaryWorkspaceWidget.setObjectName("TemporaryWorkspaceWidget")
        TemporaryWorkspaceWidget.resize(292, 155)
        TemporaryWorkspaceWidget.setStyleSheet("#label_temporary, #label_timestamp, #label_description {\n"
"    color: #999999;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(TemporaryWorkspaceWidget)
        self.verticalLayout.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_temporary = QtWidgets.QLabel(TemporaryWorkspaceWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_temporary.setFont(font)
        self.label_temporary.setAlignment(QtCore.Qt.AlignCenter)
        self.label_temporary.setObjectName("label_temporary")
        self.verticalLayout.addWidget(self.label_temporary)
        self.label_description = QtWidgets.QLabel(TemporaryWorkspaceWidget)
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setWordWrap(True)
        self.label_description.setObjectName("label_description")
        self.verticalLayout.addWidget(self.label_description)
        self.label_timestamp = QtWidgets.QLabel(TemporaryWorkspaceWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_timestamp.setFont(font)
        self.label_timestamp.setText("")
        self.label_timestamp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_timestamp.setObjectName("label_timestamp")
        self.verticalLayout.addWidget(self.label_timestamp)
        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(TemporaryWorkspaceWidget)
        QtCore.QMetaObject.connectSlotsByName(TemporaryWorkspaceWidget)

    def retranslateUi(self, TemporaryWorkspaceWidget):
        _translate = QtCore.QCoreApplication.translate
        TemporaryWorkspaceWidget.setWindowTitle(_translate("TemporaryWorkspaceWidget", "Form"))
        self.label_temporary.setText(_translate("TemporaryWorkspaceWidget", "TEXT_WORKSPACE_TEMPORARY_TITLE"))
        self.label_description.setText(_translate("TemporaryWorkspaceWidget", "TEXT_WORKSPACE_TEMPORARY_DESCRIPTION"))
