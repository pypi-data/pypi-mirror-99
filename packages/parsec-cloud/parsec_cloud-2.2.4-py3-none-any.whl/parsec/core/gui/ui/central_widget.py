# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/central_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CentralWidget(object):
    def setupUi(self, CentralWidget):
        CentralWidget.setObjectName("CentralWidget")
        CentralWidget.resize(1005, 638)
        CentralWidget.setStyleSheet("#line_2 {\n"
"    color: #DDDDDD;\n"
"}\n"
"\n"
"#label_title, #label_title2 {\n"
"    color: #999999;\n"
"}\n"
"\n"
"#label_title3 {\n"
"    background-color: #EEEEEE;\n"
"    border: none;\n"
"}\n"
"\n"
"#button_user, #button_user:hover {\n"
"    border: none;\n"
"    background: none;\n"
"    padding-right: 15px;\n"
"  color: #333333;\n"
"}\n"
"\n"
"#button_user::menu-indicator {\n"
"    image: none;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(CentralWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_menu = QtWidgets.QWidget(CentralWidget)
        self.widget_menu.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_menu.setObjectName("widget_menu")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_menu)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout.addWidget(self.widget_menu)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setContentsMargins(30, 30, 30, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_title = QtWidgets.QWidget(CentralWidget)
        self.widget_title.setObjectName("widget_title")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_title)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_title = QtWidgets.QLabel(self.widget_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        self.label_title.setMinimumSize(QtCore.QSize(0, 0))
        self.label_title.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setText("")
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_5.addWidget(self.label_title)
        self.widget_title2 = QtWidgets.QWidget(self.widget_title)
        self.widget_title2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.widget_title2.setFont(font)
        self.widget_title2.setObjectName("widget_title2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_title2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.icon_title2 = IconLabel(self.widget_title2)
        self.icon_title2.setMinimumSize(QtCore.QSize(10, 10))
        self.icon_title2.setMaximumSize(QtCore.QSize(10, 10))
        self.icon_title2.setText("")
        self.icon_title2.setPixmap(QtGui.QPixmap(":/icons/images/material/fiber_manual_record.svg"))
        self.icon_title2.setScaledContents(True)
        self.icon_title2.setProperty("color", QtGui.QColor(153, 153, 153))
        self.icon_title2.setObjectName("icon_title2")
        self.horizontalLayout_3.addWidget(self.icon_title2)
        self.label_title2 = QtWidgets.QLabel(self.widget_title2)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_title2.setFont(font)
        self.label_title2.setText("")
        self.label_title2.setObjectName("label_title2")
        self.horizontalLayout_3.addWidget(self.label_title2)
        self.horizontalLayout_5.addWidget(self.widget_title2)
        self.widget_title3 = QtWidgets.QWidget(self.widget_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_title3.sizePolicy().hasHeightForWidth())
        self.widget_title3.setSizePolicy(sizePolicy)
        self.widget_title3.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_title3.setObjectName("widget_title3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_title3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.icon_title3 = IconLabel(self.widget_title3)
        self.icon_title3.setMinimumSize(QtCore.QSize(10, 10))
        self.icon_title3.setMaximumSize(QtCore.QSize(10, 10))
        self.icon_title3.setText("")
        self.icon_title3.setPixmap(QtGui.QPixmap(":/icons/images/material/fiber_manual_record.svg"))
        self.icon_title3.setScaledContents(True)
        self.icon_title3.setProperty("color", QtGui.QColor(153, 153, 153))
        self.icon_title3.setObjectName("icon_title3")
        self.horizontalLayout_4.addWidget(self.icon_title3)
        self.label_title3 = QtWidgets.QLineEdit(self.widget_title3)
        self.label_title3.setReadOnly(True)
        self.label_title3.setObjectName("label_title3")
        self.horizontalLayout_4.addWidget(self.label_title3)
        self.horizontalLayout_5.addWidget(self.widget_title3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.button_user = QtWidgets.QToolButton(self.widget_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_user.sizePolicy().hasHeightForWidth())
        self.button_user.setSizePolicy(sizePolicy)
        self.button_user.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_user.setFont(font)
        self.button_user.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_user.setText("")
        self.button_user.setIconSize(QtCore.QSize(45, 45))
        self.button_user.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.button_user.setAutoRaise(True)
        self.button_user.setObjectName("button_user")
        self.horizontalLayout_5.addWidget(self.button_user)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.line_2 = QtWidgets.QFrame(self.widget_title)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.verticalLayout_2.addWidget(self.widget_title)
        self.widget_central = QtWidgets.QWidget(CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_central.sizePolicy().hasHeightForWidth())
        self.widget_central.setSizePolicy(sizePolicy)
        self.widget_central.setObjectName("widget_central")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_central)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_2.addWidget(self.widget_central)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.widget_notif = QtWidgets.QWidget(CentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_notif.sizePolicy().hasHeightForWidth())
        self.widget_notif.setSizePolicy(sizePolicy)
        self.widget_notif.setMinimumSize(QtCore.QSize(350, 0))
        self.widget_notif.setMaximumSize(QtCore.QSize(350, 16777215))
        self.widget_notif.setObjectName("widget_notif")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_notif)
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2.addWidget(self.widget_notif)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(CentralWidget)
        QtCore.QMetaObject.connectSlotsByName(CentralWidget)

    def retranslateUi(self, CentralWidget):
        _translate = QtCore.QCoreApplication.translate
        CentralWidget.setWindowTitle(_translate("CentralWidget", "Form"))
from parsec.core.gui.custom_widgets import IconLabel
from parsec.core.gui import resources_rc
