# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/file_history_button.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileHistoryButton(object):
    def setupUi(self, FileHistoryButton):
        FileHistoryButton.setObjectName("FileHistoryButton")
        FileHistoryButton.resize(485, 130)
        FileHistoryButton.setStyleSheet("QWidget#FileHistoryButton, #widget\n"
"{\n"
"    border-radius: 8px;\n"
"    background-color: #FFFFFF;\n"
"}\n"
"\n"
"#label_user, #label_date, #label_size, #label_src, #label_dst, #label_version {\n"
"    font-weight: bold;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(FileHistoryButton)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(FileHistoryButton)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(15)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.label_version = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_version.sizePolicy().hasHeightForWidth())
        self.label_version.setSizePolicy(sizePolicy)
        self.label_version.setText("")
        self.label_version.setObjectName("label_version")
        self.horizontalLayout_6.addWidget(self.label_version)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.label_size = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_size.sizePolicy().hasHeightForWidth())
        self.label_size.setSizePolicy(sizePolicy)
        self.label_size.setText("")
        self.label_size.setObjectName("label_size")
        self.horizontalLayout_7.addWidget(self.label_size)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.label_date = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_date.sizePolicy().hasHeightForWidth())
        self.label_date.setSizePolicy(sizePolicy)
        self.label_date.setText("")
        self.label_date.setObjectName("label_date")
        self.horizontalLayout_4.addWidget(self.label_date)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.label_user = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_user.sizePolicy().hasHeightForWidth())
        self.label_user.setSizePolicy(sizePolicy)
        self.label_user.setText("")
        self.label_user.setObjectName("label_user")
        self.horizontalLayout_3.addWidget(self.label_user)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_src = QtWidgets.QLabel(self.widget)
        self.label_src.setText("")
        self.label_src.setObjectName("label_src")
        self.horizontalLayout_2.addWidget(self.label_src)
        self.label_dst = QtWidgets.QLabel(self.widget)
        self.label_dst.setText("")
        self.label_dst.setObjectName("label_dst")
        self.horizontalLayout_2.addWidget(self.label_dst)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(FileHistoryButton)
        QtCore.QMetaObject.connectSlotsByName(FileHistoryButton)

    def retranslateUi(self, FileHistoryButton):
        _translate = QtCore.QCoreApplication.translate
        FileHistoryButton.setWindowTitle(_translate("FileHistoryButton", "Form"))
        self.label_2.setText(_translate("FileHistoryButton", "TEXT_FILE_HISTORY_VERSION"))
        self.label_4.setText(_translate("FileHistoryButton", "TEXT_FILE_HISTORY_SIZE"))
        self.label.setText(_translate("FileHistoryButton", "TEXT_FILE_HISTORY_WHEN"))
        self.label_3.setText(_translate("FileHistoryButton", "TEXT_FILE_HISTORY_BY"))
