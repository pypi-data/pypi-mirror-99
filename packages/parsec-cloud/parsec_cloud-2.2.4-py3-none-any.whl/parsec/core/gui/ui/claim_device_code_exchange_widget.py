# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/claim_device_code_exchange_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClaimDeviceCodeExchangeWidget(object):
    def setupUi(self, ClaimDeviceCodeExchangeWidget):
        ClaimDeviceCodeExchangeWidget.setObjectName("ClaimDeviceCodeExchangeWidget")
        ClaimDeviceCodeExchangeWidget.resize(486, 180)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClaimDeviceCodeExchangeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_greeter_code = QtWidgets.QWidget(ClaimDeviceCodeExchangeWidget)
        self.widget_greeter_code.setEnabled(True)
        self.widget_greeter_code.setObjectName("widget_greeter_code")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_greeter_code)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget_greeter_code)
        self.label_3.setLineWidth(0)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.layout_greeter_code = QtWidgets.QHBoxLayout()
        self.layout_greeter_code.setContentsMargins(-1, -1, 0, -1)
        self.layout_greeter_code.setObjectName("layout_greeter_code")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_greeter_code.addItem(spacerItem)
        self.code_input_widget = CodeInputWidget(self.widget_greeter_code)
        self.code_input_widget.setObjectName("code_input_widget")
        self.layout_greeter_code.addWidget(self.code_input_widget)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_greeter_code.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.layout_greeter_code)
        self.verticalLayout.addWidget(self.widget_greeter_code)
        self.widget_claimer_code = QtWidgets.QWidget(ClaimDeviceCodeExchangeWidget)
        self.widget_claimer_code.setEnabled(True)
        self.widget_claimer_code.setObjectName("widget_claimer_code")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_claimer_code)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_claimer_code)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.line_edit_claimer_code = QtWidgets.QLineEdit(self.widget_claimer_code)
        self.line_edit_claimer_code.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit_claimer_code.setReadOnly(True)
        self.line_edit_claimer_code.setObjectName("line_edit_claimer_code")
        self.horizontalLayout.addWidget(self.line_edit_claimer_code)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_wait = QtWidgets.QLabel(self.widget_claimer_code)
        self.label_wait.setAlignment(QtCore.Qt.AlignCenter)
        self.label_wait.setWordWrap(True)
        self.label_wait.setObjectName("label_wait")
        self.verticalLayout_2.addWidget(self.label_wait)
        self.verticalLayout.addWidget(self.widget_claimer_code)

        self.retranslateUi(ClaimDeviceCodeExchangeWidget)
        QtCore.QMetaObject.connectSlotsByName(ClaimDeviceCodeExchangeWidget)

    def retranslateUi(self, ClaimDeviceCodeExchangeWidget):
        _translate = QtCore.QCoreApplication.translate
        ClaimDeviceCodeExchangeWidget.setWindowTitle(_translate("ClaimDeviceCodeExchangeWidget", "Form"))
        self.label_3.setText(_translate("ClaimDeviceCodeExchangeWidget", "TEXT_CLAIM_DEVICE_CODE_EXCHANGE_GET_CODE_INSTRUCTIONS"))
        self.label_2.setText(_translate("ClaimDeviceCodeExchangeWidget", "TEXT_CLAIM_DEVICE_CODE_EXCHANGE_GIVE_CODE_INSTRUCTIONS"))
        self.label_wait.setText(_translate("ClaimDeviceCodeExchangeWidget", "TEXT_CLAIM_DEVICE_CODE_EXCHANGE_WAIT"))
from parsec.core.gui.custom_widgets import CodeInputWidget
