# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/notification_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NotificationWidget(object):
    def setupUi(self, NotificationWidget):
        NotificationWidget.setObjectName("NotificationWidget")
        NotificationWidget.resize(307, 134)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NotificationWidget.sizePolicy().hasHeightForWidth())
        NotificationWidget.setSizePolicy(sizePolicy)
        NotificationWidget.setMinimumSize(QtCore.QSize(0, 0))
        NotificationWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(NotificationWidget)
        self.verticalLayout.setContentsMargins(0, 5, 0, 20)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_close = QtWidgets.QPushButton(NotificationWidget)
        self.button_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/icons/menu_cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon)
        self.button_close.setIconSize(QtCore.QSize(20, 20))
        self.button_close.setFlat(True)
        self.button_close.setObjectName("button_close")
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_icon = QtWidgets.QLabel(NotificationWidget)
        self.label_icon.setMinimumSize(QtCore.QSize(40, 40))
        self.label_icon.setMaximumSize(QtCore.QSize(40, 40))
        self.label_icon.setText("")
        self.label_icon.setScaledContents(True)
        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout_2.addWidget(self.label_icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_date = QtWidgets.QLabel(NotificationWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_date.setFont(font)
        self.label_date.setText("")
        self.label_date.setObjectName("label_date")
        self.verticalLayout_2.addWidget(self.label_date)
        self.label_message = QtWidgets.QLabel(NotificationWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_message.sizePolicy().hasHeightForWidth())
        self.label_message.setSizePolicy(sizePolicy)
        self.label_message.setMinimumSize(QtCore.QSize(220, 40))
        self.label_message.setMaximumSize(QtCore.QSize(220, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_message.setFont(font)
        self.label_message.setText("")
        self.label_message.setWordWrap(True)
        self.label_message.setObjectName("label_message")
        self.verticalLayout_2.addWidget(self.label_message)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(NotificationWidget)
        QtCore.QMetaObject.connectSlotsByName(NotificationWidget)

    def retranslateUi(self, NotificationWidget):
        _translate = QtCore.QCoreApplication.translate
        NotificationWidget.setWindowTitle(_translate("NotificationWidget", "Form"))
from parsec.core.gui import resources_rc
