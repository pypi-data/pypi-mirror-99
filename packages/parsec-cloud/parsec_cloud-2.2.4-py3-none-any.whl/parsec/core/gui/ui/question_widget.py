# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/question_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QuestionWidget(object):
    def setupUi(self, QuestionWidget):
        QuestionWidget.setObjectName("QuestionWidget")
        QuestionWidget.resize(250, 111)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QuestionWidget.sizePolicy().hasHeightForWidth())
        QuestionWidget.setSizePolicy(sizePolicy)
        QuestionWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        QuestionWidget.setStyleSheet("QPushButton {\n"
"    text-transform: uppercase;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(QuestionWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_message = QtWidgets.QLabel(QuestionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_message.sizePolicy().hasHeightForWidth())
        self.label_message.setSizePolicy(sizePolicy)
        self.label_message.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_message.setText("")
        self.label_message.setTextFormat(QtCore.Qt.RichText)
        self.label_message.setWordWrap(True)
        self.label_message.setObjectName("label_message")
        self.horizontalLayout.addWidget(self.label_message)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.layout_radios = QtWidgets.QVBoxLayout()
        self.layout_radios.setSpacing(20)
        self.layout_radios.setObjectName("layout_radios")
        self.verticalLayout.addLayout(self.layout_radios)
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.layout_buttons.setContentsMargins(-1, 0, -1, -1)
        self.layout_buttons.setSpacing(10)
        self.layout_buttons.setObjectName("layout_buttons")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_buttons.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.layout_buttons)

        self.retranslateUi(QuestionWidget)
        QtCore.QMetaObject.connectSlotsByName(QuestionWidget)

    def retranslateUi(self, QuestionWidget):
        _translate = QtCore.QCoreApplication.translate
        QuestionWidget.setWindowTitle(_translate("QuestionWidget", "Form"))
