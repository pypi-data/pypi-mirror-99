# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/workspaces_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WorkspacesWidget(object):
    def setupUi(self, WorkspacesWidget):
        WorkspacesWidget.setObjectName("WorkspacesWidget")
        WorkspacesWidget.resize(636, 428)
        WorkspacesWidget.setMinimumSize(QtCore.QSize(0, 0))
        WorkspacesWidget.setStyleSheet("#button_goto_file, #button_add_workspace {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #0092FF;\n"
"}\n"
"\n"
"#button_goto_file:hover, #button_add_workspace:hover {\n"
"    color: #0070DD;\n"
"}\n"
"\n"
"#scrollAreaWidgetContents {\n"
"    background-color: #EEEEEE;\n"
"}\n"
"\n"
"#filter_widget {\n"
"    border-radius: 5px;\n"
"    background-color: #CCCCCC;\n"
"}\n"
"\n"
"#filter_label {\n"
"    color: #888888;\n"
"}\n"
"\n"
"#filter_remove_button, filter_remove_button:hover {\n"
"    background-color: #CCCCCC;\n"
"    padding: 0;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(WorkspacesWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(WorkspacesWidget)
        self.line_edit_search.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)
        self.button_add_workspace = Button(WorkspacesWidget)
        self.button_add_workspace.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/add_to_queue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_workspace.setIcon(icon)
        self.button_add_workspace.setIconSize(QtCore.QSize(24, 24))
        self.button_add_workspace.setFlat(True)
        self.button_add_workspace.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_add_workspace.setObjectName("button_add_workspace")
        self.horizontalLayout.addWidget(self.button_add_workspace)
        self.button_goto_file = Button(WorkspacesWidget)
        self.button_goto_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/material/subdirectory_arrow_right.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_goto_file.setIcon(icon1)
        self.button_goto_file.setIconSize(QtCore.QSize(24, 24))
        self.button_goto_file.setFlat(True)
        self.button_goto_file.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_goto_file.setObjectName("button_goto_file")
        self.horizontalLayout.addWidget(self.button_goto_file)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.filter_layout_widget = QtWidgets.QWidget(WorkspacesWidget)
        self.filter_layout_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.filter_layout_widget.setObjectName("filter_layout_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.filter_layout_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.filter_widget = QtWidgets.QWidget(self.filter_layout_widget)
        self.filter_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.filter_widget.setObjectName("filter_widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.filter_widget)
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.filter_label = QtWidgets.QLabel(self.filter_widget)
        self.filter_label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.filter_label.setFont(font)
        self.filter_label.setText("")
        self.filter_label.setObjectName("filter_label")
        self.horizontalLayout_3.addWidget(self.filter_label)
        self.filter_remove_button = Button(self.filter_widget)
        self.filter_remove_button.setMinimumSize(QtCore.QSize(28, 28))
        self.filter_remove_button.setMaximumSize(QtCore.QSize(28, 28))
        self.filter_remove_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/images/material/close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filter_remove_button.setIcon(icon2)
        self.filter_remove_button.setIconSize(QtCore.QSize(24, 24))
        self.filter_remove_button.setDefault(True)
        self.filter_remove_button.setFlat(True)
        self.filter_remove_button.setProperty("color", QtGui.QColor(136, 136, 136))
        self.filter_remove_button.setProperty("hover_color", QtGui.QColor(102, 102, 102))
        self.filter_remove_button.setObjectName("filter_remove_button")
        self.horizontalLayout_3.addWidget(self.filter_remove_button)
        self.horizontalLayout_4.addWidget(self.filter_widget)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_5.addWidget(self.filter_layout_widget)
        self.verticalLayout.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.spinner = SpinnerWidget(WorkspacesWidget)
        self.spinner.setMinimumSize(QtCore.QSize(200, 200))
        self.spinner.setMaximumSize(QtCore.QSize(200, 200))
        self.spinner.setObjectName("spinner")
        self.horizontalLayout_2.addWidget(self.spinner)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(WorkspacesWidget)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 636, 91))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setContentsMargins(0, 0, 4, 0)
        self.layout_content.setSpacing(20)
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout_2.addLayout(self.layout_content)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)

        self.retranslateUi(WorkspacesWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkspacesWidget)

    def retranslateUi(self, WorkspacesWidget):
        _translate = QtCore.QCoreApplication.translate
        WorkspacesWidget.setWindowTitle(_translate("WorkspacesWidget", "Form"))
        self.line_edit_search.setPlaceholderText(_translate("WorkspacesWidget", "TEXT_WORKSPACE_FILTER_WORKSPACES_PLACEHOLDER"))
        self.button_add_workspace.setText(_translate("WorkspacesWidget", "ACTION_WORKSPACE_ADD_WORKSPACE"))
        self.button_goto_file.setText(_translate("WorkspacesWidget", "ACTION_WORKSPACE_GOTO_FILE_LINK"))
from parsec.core.gui.custom_widgets import Button, SpinnerWidget
from parsec.core.gui import resources_rc
