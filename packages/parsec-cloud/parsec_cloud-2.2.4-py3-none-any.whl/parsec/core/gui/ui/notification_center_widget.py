# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/notification_center_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NotificationCenterWidget(object):
    def setupUi(self, NotificationCenterWidget):
        NotificationCenterWidget.setObjectName("NotificationCenterWidget")
        NotificationCenterWidget.resize(350, 430)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NotificationCenterWidget.sizePolicy().hasHeightForWidth())
        NotificationCenterWidget.setSizePolicy(sizePolicy)
        NotificationCenterWidget.setMinimumSize(QtCore.QSize(350, 0))
        NotificationCenterWidget.setMaximumSize(QtCore.QSize(350, 16777215))
        NotificationCenterWidget.setStyleSheet("QWidget#NotificationCenterWidget\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"background: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"background: rgb(12, 65, 157);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical\n"
"{\n"
"border: none;\n"
"background: none;\n"
"}\n"
"\n"
"#button_close\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"border: 0;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(NotificationCenterWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 4, 4, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_close = QtWidgets.QPushButton(NotificationCenterWidget)
        self.button_close.setStyleSheet("")
        self.button_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/icons/menu_cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon)
        self.button_close.setIconSize(QtCore.QSize(20, 20))
        self.button_close.setFlat(True)
        self.button_close.setObjectName("button_close")
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 0, 10, -1)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(NotificationCenterWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.line = QtWidgets.QFrame(NotificationCenterWidget)
        self.line.setStyleSheet("color: rgb(11, 65, 155);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.scrollArea = QtWidgets.QScrollArea(NotificationCenterWidget)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.widget_layout = QtWidgets.QWidget()
        self.widget_layout.setGeometry(QtCore.QRect(0, 0, 330, 365))
        self.widget_layout.setStyleSheet("QWidget#widget_layout\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget_layout.setObjectName("widget_layout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_layout)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.scrollArea.setWidget(self.widget_layout)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(NotificationCenterWidget)
        QtCore.QMetaObject.connectSlotsByName(NotificationCenterWidget)

    def retranslateUi(self, NotificationCenterWidget):
        _translate = QtCore.QCoreApplication.translate
        NotificationCenterWidget.setWindowTitle(_translate("NotificationCenterWidget", "Form"))
        self.label.setText(_translate("NotificationCenterWidget", "LABEL_NOTIFICATIONS"))
from parsec.core.gui import resources_rc
