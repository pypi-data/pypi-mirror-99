# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/input_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InputWidget(object):
    def setupUi(self, InputWidget):
        InputWidget.setObjectName("InputWidget")
        InputWidget.resize(324, 127)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InputWidget.sizePolicy().hasHeightForWidth())
        InputWidget.setSizePolicy(sizePolicy)
        InputWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        InputWidget.setStyleSheet("QPushButton {\n"
"    text-transform: uppercase;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(InputWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_message = QtWidgets.QLabel(InputWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_message.sizePolicy().hasHeightForWidth())
        self.label_message.setSizePolicy(sizePolicy)
        self.label_message.setMinimumSize(QtCore.QSize(0, 0))
        self.label_message.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_message.setText("")
        self.label_message.setTextFormat(QtCore.Qt.RichText)
        self.label_message.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_message.setWordWrap(True)
        self.label_message.setObjectName("label_message")
        self.horizontalLayout_3.addWidget(self.label_message)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line_edit_text = ValidatedLineEdit(InputWidget)
        self.line_edit_text.setObjectName("line_edit_text")
        self.verticalLayout.addWidget(self.line_edit_text)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_ok = QtWidgets.QPushButton(InputWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_ok.sizePolicy().hasHeightForWidth())
        self.button_ok.setSizePolicy(sizePolicy)
        self.button_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_ok.setText("")
        self.button_ok.setObjectName("button_ok")
        self.horizontalLayout_2.addWidget(self.button_ok)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(InputWidget)
        QtCore.QMetaObject.connectSlotsByName(InputWidget)

    def retranslateUi(self, InputWidget):
        _translate = QtCore.QCoreApplication.translate
        InputWidget.setWindowTitle(_translate("InputWidget", "Form"))
from parsec.core.gui.input_widgets import ValidatedLineEdit
