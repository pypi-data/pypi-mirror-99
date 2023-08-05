# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/password_choice_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PasswordChoiceWidget(object):
    def setupUi(self, PasswordChoiceWidget):
        PasswordChoiceWidget.setObjectName("PasswordChoiceWidget")
        PasswordChoiceWidget.resize(400, 210)
        PasswordChoiceWidget.setMinimumSize(QtCore.QSize(0, 210))
        PasswordChoiceWidget.setStyleSheet("#label_mismatch {\n"
"    color: #F1962B;\n"
"}\n"
"\n"
"#label_password_warning {\n"
"    color: #F1962B;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(PasswordChoiceWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_password_warning = QtWidgets.QLabel(PasswordChoiceWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_password_warning.setFont(font)
        self.label_password_warning.setAlignment(QtCore.Qt.AlignCenter)
        self.label_password_warning.setWordWrap(True)
        self.label_password_warning.setObjectName("label_password_warning")
        self.verticalLayout.addWidget(self.label_password_warning)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setSpacing(5)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_password = QtWidgets.QLabel(PasswordChoiceWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_password.setFont(font)
        self.label_password.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_password.setObjectName("label_password")
        self.verticalLayout_14.addWidget(self.label_password)
        self.line_edit_password = QtWidgets.QLineEdit(PasswordChoiceWidget)
        self.line_edit_password.setMinimumSize(QtCore.QSize(0, 0))
        self.line_edit_password.setText("")
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_password.setPlaceholderText("")
        self.line_edit_password.setObjectName("line_edit_password")
        self.verticalLayout_14.addWidget(self.line_edit_password)
        self.verticalLayout.addLayout(self.verticalLayout_14)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setSpacing(5)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_confirmation = QtWidgets.QLabel(PasswordChoiceWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_confirmation.setFont(font)
        self.label_confirmation.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_confirmation.setObjectName("label_confirmation")
        self.verticalLayout_15.addWidget(self.label_confirmation)
        self.line_edit_password_check = QtWidgets.QLineEdit(PasswordChoiceWidget)
        self.line_edit_password_check.setMinimumSize(QtCore.QSize(0, 0))
        self.line_edit_password_check.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_password_check.setPlaceholderText("")
        self.line_edit_password_check.setObjectName("line_edit_password_check")
        self.verticalLayout_15.addWidget(self.line_edit_password_check)
        self.label_mismatch = QtWidgets.QLabel(PasswordChoiceWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_mismatch.setFont(font)
        self.label_mismatch.setWordWrap(True)
        self.label_mismatch.setObjectName("label_mismatch")
        self.verticalLayout_15.addWidget(self.label_mismatch)
        self.verticalLayout.addLayout(self.verticalLayout_15)
        self.layout_password_strength = QtWidgets.QHBoxLayout()
        self.layout_password_strength.setObjectName("layout_password_strength")
        self.verticalLayout.addLayout(self.layout_password_strength)

        self.retranslateUi(PasswordChoiceWidget)
        QtCore.QMetaObject.connectSlotsByName(PasswordChoiceWidget)

    def retranslateUi(self, PasswordChoiceWidget):
        _translate = QtCore.QCoreApplication.translate
        PasswordChoiceWidget.setWindowTitle(_translate("PasswordChoiceWidget", "Form"))
        self.label_password_warning.setText(_translate("PasswordChoiceWidget", "TEXT_PASSWORD_WARNING"))
        self.label_password.setText(_translate("PasswordChoiceWidget", "TEXT_LABEL_PASSWORD"))
        self.label_confirmation.setText(_translate("PasswordChoiceWidget", "TEXT_LABEL_PASSWORD_CONFIRMATION"))
        self.label_mismatch.setText(_translate("PasswordChoiceWidget", "TEXT_PASSWORD_CHOICE_MISMATCH"))
