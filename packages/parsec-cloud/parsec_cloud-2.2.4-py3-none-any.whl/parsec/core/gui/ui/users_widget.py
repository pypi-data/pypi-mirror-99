# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/users_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UsersWidget(object):
    def setupUi(self, UsersWidget):
        UsersWidget.setObjectName("UsersWidget")
        UsersWidget.resize(624, 524)
        UsersWidget.setStyleSheet("#button_add_user, #button_next_page, #button_previous_page {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #0092FF;\n"
"}\n"
"\n"
"#button_add_user:hover {\n"
"    color: #0070DD;\n"
"}\n"
"\n"
"#button_next_page:hover, #button_previous_page:hover {\n"
"    color: #0070DD;\n"
"    text-decoration: underline;\n"
"}\n"
"\n"
"#button_next_page:disabled, #button_previous_page:disabled {\n"
"    color: #999999;\n"
"}\n"
"\n"
"#scrollAreaWidgetContents {\n"
"    background-color: #EEEEEE;\n"
"}\n"
"\n"
"#label_page_info {\n"
"    color: #999999;\n"
"    font-weight: bold;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(UsersWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(UsersWidget)
        self.line_edit_search.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setText("")
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)
        self.button_users_filter = QtWidgets.QPushButton(UsersWidget)
        self.button_users_filter.setObjectName("button_users_filter")
        self.horizontalLayout.addWidget(self.button_users_filter)
        self.button_add_user = Button(UsersWidget)
        self.button_add_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/person_add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_user.setIcon(icon)
        self.button_add_user.setIconSize(QtCore.QSize(24, 24))
        self.button_add_user.setFlat(True)
        self.button_add_user.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_add_user.setObjectName("button_add_user")
        self.horizontalLayout.addWidget(self.button_add_user)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(UsersWidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 622, 456))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setContentsMargins(0, 0, 4, -1)
        self.layout_content.setSpacing(20)
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout_2.addLayout(self.layout_content)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinner = SpinnerWidget(self.scrollAreaWidgetContents)
        self.spinner.setObjectName("spinner")
        self.horizontalLayout_2.addWidget(self.spinner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.PaginationHorizontalLayout = QtWidgets.QHBoxLayout()
        self.PaginationHorizontalLayout.setSpacing(15)
        self.PaginationHorizontalLayout.setObjectName("PaginationHorizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.PaginationHorizontalLayout.addItem(spacerItem3)
        self.button_previous_page = Button(UsersWidget)
        self.button_previous_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_previous_page.setObjectName("button_previous_page")
        self.PaginationHorizontalLayout.addWidget(self.button_previous_page)
        self.label_page_info = QtWidgets.QLabel(UsersWidget)
        self.label_page_info.setText("")
        self.label_page_info.setObjectName("label_page_info")
        self.PaginationHorizontalLayout.addWidget(self.label_page_info)
        self.button_next_page = Button(UsersWidget)
        self.button_next_page.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_next_page.setObjectName("button_next_page")
        self.PaginationHorizontalLayout.addWidget(self.button_next_page)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.PaginationHorizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.PaginationHorizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)

        self.retranslateUi(UsersWidget)
        QtCore.QMetaObject.connectSlotsByName(UsersWidget)

    def retranslateUi(self, UsersWidget):
        _translate = QtCore.QCoreApplication.translate
        UsersWidget.setWindowTitle(_translate("UsersWidget", "Form"))
        self.line_edit_search.setPlaceholderText(_translate("UsersWidget", "TEXT_USERS_FILTER_USERS_PLACEHOLDER"))
        self.button_users_filter.setText(_translate("UsersWidget", "ACTION_FILTER_LIST_USERS"))
        self.button_add_user.setText(_translate("UsersWidget", "ACTION_USER_INVITE_USER"))
        self.button_previous_page.setText(_translate("UsersWidget", "ACTION_LIST_PREVIOUS_PAGE"))
        self.button_next_page.setText(_translate("UsersWidget", "ACTION_LIST_NEXT_PAGE"))
from parsec.core.gui.custom_widgets import Button, SpinnerWidget
from parsec.core.gui import resources_rc
