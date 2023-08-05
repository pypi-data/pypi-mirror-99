# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/workspace_sharing_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WorkspaceSharingWidget(object):
    def setupUi(self, WorkspaceSharingWidget):
        WorkspaceSharingWidget.setObjectName("WorkspaceSharingWidget")
        WorkspaceSharingWidget.resize(474, 468)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WorkspaceSharingWidget.sizePolicy().hasHeightForWidth())
        WorkspaceSharingWidget.setSizePolicy(sizePolicy)
        WorkspaceSharingWidget.setStyleSheet("#WorkspaceSharingWidget {\n"
"    background-color: #F4F4F4;\n"
"}\n"
"\n"
"#scroll_content, #widget_users {\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#button_share, #button_apply {\n"
"    text-transform: uppercase;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(WorkspaceSharingWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.line_edit_filter = QtWidgets.QLineEdit(WorkspaceSharingWidget)
        self.line_edit_filter.setObjectName("line_edit_filter")
        self.horizontalLayout_3.addWidget(self.line_edit_filter)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.spinner = SpinnerWidget(WorkspaceSharingWidget)
        self.spinner.setObjectName("spinner")
        self.horizontalLayout.addWidget(self.spinner)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget_users = QtWidgets.QWidget(WorkspaceSharingWidget)
        self.widget_users.setMinimumSize(QtCore.QSize(400, 250))
        self.widget_users.setObjectName("widget_users")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_users)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_users)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_content.setGeometry(QtCore.QRect(0, 0, 474, 379))
        self.scroll_content.setObjectName("scroll_content")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scroll_content)
        self.verticalLayout_3.setContentsMargins(20, 10, 0, 10)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.scrollArea.setWidget(self.scroll_content)
        self.verticalLayout_5.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.widget_users)

        self.retranslateUi(WorkspaceSharingWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkspaceSharingWidget)

    def retranslateUi(self, WorkspaceSharingWidget):
        _translate = QtCore.QCoreApplication.translate
        self.line_edit_filter.setPlaceholderText(_translate("WorkspaceSharingWidget", "TEXT_USERS_FILTER_USERS_PLACEHOLDER"))
from parsec.core.gui.custom_widgets import SpinnerWidget
