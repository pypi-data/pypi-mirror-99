# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/greet_user_code_exchange_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GreetUserCodeExchangeWidget(object):
    def setupUi(self, GreetUserCodeExchangeWidget):
        GreetUserCodeExchangeWidget.setObjectName("GreetUserCodeExchangeWidget")
        GreetUserCodeExchangeWidget.resize(479, 216)
        self.verticalLayout = QtWidgets.QVBoxLayout(GreetUserCodeExchangeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_greeter_code = QtWidgets.QWidget(GreetUserCodeExchangeWidget)
        self.widget_greeter_code.setEnabled(True)
        self.widget_greeter_code.setObjectName("widget_greeter_code")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_greeter_code)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_greeter_code)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.line_edit_greeter_code = QtWidgets.QLineEdit(self.widget_greeter_code)
        self.line_edit_greeter_code.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit_greeter_code.setReadOnly(True)
        self.line_edit_greeter_code.setObjectName("line_edit_greeter_code")
        self.horizontalLayout.addWidget(self.line_edit_greeter_code)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_wait = QtWidgets.QLabel(self.widget_greeter_code)
        self.label_wait.setAlignment(QtCore.Qt.AlignCenter)
        self.label_wait.setWordWrap(True)
        self.label_wait.setObjectName("label_wait")
        self.verticalLayout_2.addWidget(self.label_wait)
        self.verticalLayout.addWidget(self.widget_greeter_code)
        self.widget_claimer_code = QtWidgets.QWidget(GreetUserCodeExchangeWidget)
        self.widget_claimer_code.setEnabled(True)
        self.widget_claimer_code.setObjectName("widget_claimer_code")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_claimer_code)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget_claimer_code)
        self.label_3.setLineWidth(0)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(-1, -1, 0, -1)
        self.layout.setObjectName("layout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem2)
        self.code_input_widget = CodeInputWidget(self.widget_claimer_code)
        self.code_input_widget.setObjectName("code_input_widget")
        self.layout.addWidget(self.code_input_widget)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.layout)
        self.verticalLayout.addWidget(self.widget_claimer_code)

        self.retranslateUi(GreetUserCodeExchangeWidget)
        QtCore.QMetaObject.connectSlotsByName(GreetUserCodeExchangeWidget)

    def retranslateUi(self, GreetUserCodeExchangeWidget):
        _translate = QtCore.QCoreApplication.translate
        GreetUserCodeExchangeWidget.setWindowTitle(_translate("GreetUserCodeExchangeWidget", "Form"))
        self.label_2.setText(_translate("GreetUserCodeExchangeWidget", "TEXT_GREET_USER_CODE_EXCHANGE_GIVE_CODE_INSTRUCTIONS"))
        self.label_wait.setText(_translate("GreetUserCodeExchangeWidget", "TEXT_GREET_USER_CODE_EXCHANGE_WAIT"))
        self.label_3.setText(_translate("GreetUserCodeExchangeWidget", "TEXT_GREET_USER_CODE_EXCHANGE_GET_CODE_INSTRUCTIONS"))
from parsec.core.gui.custom_widgets import CodeInputWidget
