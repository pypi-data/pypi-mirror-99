# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/create_org_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateOrgWidget(object):
    def setupUi(self, CreateOrgWidget):
        CreateOrgWidget.setObjectName("CreateOrgWidget")
        CreateOrgWidget.resize(634, 539)
        CreateOrgWidget.setStyleSheet("#scrollAreaWidgetContents {\n"
"    background-color: #F4F4F4;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateOrgWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_instructions = QtWidgets.QLabel(CreateOrgWidget)
        self.label_instructions.setWordWrap(True)
        self.label_instructions.setObjectName("label_instructions")
        self.horizontalLayout_4.addWidget(self.label_instructions)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(CreateOrgWidget)
        self.label.setMinimumSize(QtCore.QSize(188, 121))
        self.label.setMaximumSize(QtCore.QSize(188, 121))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/images/logos/parsec_new.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.scrollArea = QtWidgets.QScrollArea(CreateOrgWidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 429, 451))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(-1, -1, 10, -1)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.verticalLayout_2.addLayout(self.main_layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_previous = QtWidgets.QPushButton(CreateOrgWidget)
        self.button_previous.setFlat(True)
        self.button_previous.setObjectName("button_previous")
        self.horizontalLayout_2.addWidget(self.button_previous)
        self.button_validate = QtWidgets.QPushButton(CreateOrgWidget)
        self.button_validate.setFlat(True)
        self.button_validate.setObjectName("button_validate")
        self.horizontalLayout_2.addWidget(self.button_validate)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CreateOrgWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateOrgWidget)

    def retranslateUi(self, CreateOrgWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateOrgWidget.setWindowTitle(_translate("CreateOrgWidget", "Form"))
        self.label_instructions.setText(_translate("CreateOrgWidget", "TEXT_CREATE_ORGANIZATION_INSTRUCTIONS"))
        self.button_previous.setText(_translate("CreateOrgWidget", "ACTION_PREVIOUS"))
        self.button_validate.setText(_translate("CreateOrgWidget", "ACTION_NEXT"))
from parsec.core.gui import resources_rc
