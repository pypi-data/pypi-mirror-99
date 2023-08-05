# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/menu_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MenuWidget(object):
    def setupUi(self, MenuWidget):
        MenuWidget.setObjectName("MenuWidget")
        MenuWidget.resize(260, 689)
        MenuWidget.setMinimumSize(QtCore.QSize(260, 0))
        MenuWidget.setMaximumSize(QtCore.QSize(260, 16777215))
        MenuWidget.setStyleSheet("QWidget#widget_menu {\n"
"    background-color: #222222;\n"
"}\n"
"\n"
"#button_devices, #button_files, #button_users {\n"
"    color: #999999;\n"
"    background-color: #222222;\n"
"    text-align: left;\n"
"    padding-left: 10px;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"#button_devices:checked, #button_files:checked, #button_users:checked {\n"
"    background-color: #333333;\n"
"    border: 0;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"#button_devices:hover, #button_files:hover, #button_users:hover {\n"
"    color: #EEEEEE;\n"
"}\n"
"\n"
"#label_connection_state {\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"#label_organization_name {\n"
"    color:#EEEEEE;\n"
"}\n"
"\n"
"#label_organization_size {\n"
"    color: #EEEEEE;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(MenuWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_menu = QtWidgets.QWidget(MenuWidget)
        self.widget_menu.setMinimumSize(QtCore.QSize(200, 0))
        self.widget_menu.setObjectName("widget_menu")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_menu)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_3 = QtWidgets.QWidget(self.widget_menu)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 60))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setContentsMargins(20, 20, 10, 40)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.widget_3)
        self.label.setMinimumSize(QtCore.QSize(208, 36))
        self.label.setMaximumSize(QtCore.QSize(208, 36))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/images/logos/parsec_vert.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.button_files = MenuButton(self.widget_menu)
        self.button_files.setEnabled(True)
        self.button_files.setMinimumSize(QtCore.QSize(0, 64))
        self.button_files.setMaximumSize(QtCore.QSize(16777215, 64))
        self.button_files.setBaseSize(QtCore.QSize(64, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.button_files.setFont(font)
        self.button_files.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/folder_open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_files.setIcon(icon)
        self.button_files.setIconSize(QtCore.QSize(32, 32))
        self.button_files.setCheckable(True)
        self.button_files.setFlat(True)
        self.button_files.setProperty("checked_color", QtGui.QColor(27, 141, 215))
        self.button_files.setProperty("unchecked_color", QtGui.QColor(153, 153, 153))
        self.button_files.setObjectName("button_files")
        self.verticalLayout_3.addWidget(self.button_files)
        self.button_users = MenuButton(self.widget_menu)
        self.button_users.setEnabled(True)
        self.button_users.setMinimumSize(QtCore.QSize(0, 64))
        self.button_users.setMaximumSize(QtCore.QSize(16777215, 64))
        self.button_users.setBaseSize(QtCore.QSize(0, 64))
        self.button_users.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/material/supervisor_account.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_users.setIcon(icon1)
        self.button_users.setIconSize(QtCore.QSize(32, 32))
        self.button_users.setCheckable(True)
        self.button_users.setFlat(True)
        self.button_users.setProperty("checked_color", QtGui.QColor(27, 141, 215))
        self.button_users.setProperty("unchecked_color", QtGui.QColor(153, 153, 153))
        self.button_users.setObjectName("button_users")
        self.verticalLayout_3.addWidget(self.button_users)
        self.button_devices = MenuButton(self.widget_menu)
        self.button_devices.setEnabled(True)
        self.button_devices.setMinimumSize(QtCore.QSize(0, 64))
        self.button_devices.setMaximumSize(QtCore.QSize(16777215, 64))
        self.button_devices.setBaseSize(QtCore.QSize(0, 64))
        self.button_devices.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/images/material/devices.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_devices.setIcon(icon2)
        self.button_devices.setIconSize(QtCore.QSize(32, 32))
        self.button_devices.setCheckable(True)
        self.button_devices.setChecked(False)
        self.button_devices.setFlat(True)
        self.button_devices.setProperty("checked_color", QtGui.QColor(27, 141, 215))
        self.button_devices.setProperty("unchecked_color", QtGui.QColor(153, 153, 153))
        self.button_devices.setObjectName("button_devices")
        self.verticalLayout_3.addWidget(self.button_devices)
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_3.addItem(spacerItem)
        self.widget_misc = QtWidgets.QWidget(self.widget_menu)
        self.widget_misc.setObjectName("widget_misc")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_misc)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(40)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_organization_stats = QtWidgets.QWidget(self.widget_misc)
        self.widget_organization_stats.setObjectName("widget_organization_stats")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_organization_stats)
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_organization_name = QtWidgets.QLabel(self.widget_organization_stats)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_organization_name.setFont(font)
        self.label_organization_name.setText("")
        self.label_organization_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_organization_name.setWordWrap(True)
        self.label_organization_name.setObjectName("label_organization_name")
        self.verticalLayout_4.addWidget(self.label_organization_name)
        self.label_organization_size = QtWidgets.QLabel(self.widget_organization_stats)
        self.label_organization_size.setMaximumSize(QtCore.QSize(300, 300))
        self.label_organization_size.setText("")
        self.label_organization_size.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_organization_size.setWordWrap(True)
        self.label_organization_size.setObjectName("label_organization_size")
        self.verticalLayout_4.addWidget(self.label_organization_size)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addWidget(self.widget_organization_stats)
        self.widget_connection = QtWidgets.QWidget(self.widget_misc)
        self.widget_connection.setObjectName("widget_connection")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_connection)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.icon_connection = IconLabel(self.widget_connection)
        self.icon_connection.setMinimumSize(QtCore.QSize(32, 32))
        self.icon_connection.setMaximumSize(QtCore.QSize(32, 32))
        self.icon_connection.setText("")
        self.icon_connection.setPixmap(QtGui.QPixmap(":/icons/images/material/cloud_off.svg"))
        self.icon_connection.setScaledContents(True)
        self.icon_connection.setProperty("color", QtGui.QColor(27, 141, 215))
        self.icon_connection.setObjectName("icon_connection")
        self.horizontalLayout_6.addWidget(self.icon_connection)
        self.label_connection_state = QtWidgets.QLabel(self.widget_connection)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_connection_state.setFont(font)
        self.label_connection_state.setText("")
        self.label_connection_state.setObjectName("label_connection_state")
        self.horizontalLayout_6.addWidget(self.label_connection_state)
        self.verticalLayout_2.addWidget(self.widget_connection)
        self.verticalLayout_3.addWidget(self.widget_misc)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_8.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.widget_menu)

        self.retranslateUi(MenuWidget)
        QtCore.QMetaObject.connectSlotsByName(MenuWidget)

    def retranslateUi(self, MenuWidget):
        _translate = QtCore.QCoreApplication.translate
        MenuWidget.setWindowTitle(_translate("MenuWidget", "Form"))
        self.button_files.setText(_translate("MenuWidget", "ACTION_MENU_DOCUMENTS"))
        self.button_users.setText(_translate("MenuWidget", "ACTION_MENU_USERS"))
        self.button_devices.setText(_translate("MenuWidget", "ACTION_MENU_DEVICES"))
from parsec.core.gui.custom_widgets import IconLabel, MenuButton
from parsec.core.gui import resources_rc
