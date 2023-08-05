# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/greyed_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GreyedDialog(object):
    def setupUi(self, GreyedDialog):
        GreyedDialog.setObjectName("GreyedDialog")
        GreyedDialog.resize(519, 238)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GreyedDialog.sizePolicy().hasHeightForWidth())
        GreyedDialog.setSizePolicy(sizePolicy)
        GreyedDialog.setStyleSheet("#GreyedDialog {\n"
"    background-color: rgba(51, 51, 51, 204);\n"
"}\n"
"\n"
"#MainWidget {\n"
"    background-color: #F4F4F4;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#button_close {\n"
"    background-color: none;\n"
"    border: none;\n"
"}")
        GreyedDialog.setModal(True)
        self.vertical_layout = QtWidgets.QVBoxLayout(GreyedDialog)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setObjectName("vertical_layout")
        spacerItem = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout.addItem(spacerItem)
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setObjectName("horizontal_layout")
        spacerItem1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem1)
        self.MainWidget = QtWidgets.QWidget(GreyedDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWidget.sizePolicy().hasHeightForWidth())
        self.MainWidget.setSizePolicy(sizePolicy)
        self.MainWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.MainWidget.setObjectName("MainWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.MainWidget)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_3.setContentsMargins(40, 40, 40, 40)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_title = QtWidgets.QWidget(self.MainWidget)
        self.widget_title.setMinimumSize(QtCore.QSize(200, 0))
        self.widget_title.setObjectName("widget_title")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_title)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_title = QtWidgets.QLabel(self.widget_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setText("")
        self.label_title.setWordWrap(True)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_3.addWidget(self.label_title)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.button_close = Button(self.widget_title)
        self.button_close.setMinimumSize(QtCore.QSize(32, 32))
        self.button_close.setMaximumSize(QtCore.QSize(32, 32))
        self.button_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_close.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.button_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon)
        self.button_close.setIconSize(QtCore.QSize(24, 24))
        self.button_close.setFlat(True)
        self.button_close.setProperty("color", QtGui.QColor(51, 51, 51))
        self.button_close.setProperty("hover_color", QtGui.QColor(0, 0, 0))
        self.button_close.setObjectName("button_close")
        self.horizontalLayout_3.addWidget(self.button_close)
        self.horizontalLayout_2.addWidget(self.widget_title)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_layout.setContentsMargins(-1, 20, -1, -1)
        self.main_layout.setObjectName("main_layout")
        self.verticalLayout_3.addLayout(self.main_layout)
        self.horizontal_layout.addWidget(self.MainWidget)
        spacerItem3 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem3)
        self.vertical_layout.addLayout(self.horizontal_layout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout.addItem(spacerItem4)

        self.retranslateUi(GreyedDialog)
        self.button_close.clicked.connect(GreyedDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GreyedDialog)

    def retranslateUi(self, GreyedDialog):
        _translate = QtCore.QCoreApplication.translate
        GreyedDialog.setWindowTitle(_translate("GreyedDialog", "Dialog"))
        self.button_close.setToolTip(_translate("GreyedDialog", "TEXT_DIALOG_CLOSE_TOOLTIP"))
from parsec.core.gui.custom_widgets import Button
from parsec.core.gui import resources_rc
