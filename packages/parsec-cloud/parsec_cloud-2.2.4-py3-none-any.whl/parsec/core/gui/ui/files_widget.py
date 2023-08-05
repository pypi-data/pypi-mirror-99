# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/files_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FilesWidget(object):
    def setupUi(self, FilesWidget):
        FilesWidget.setObjectName("FilesWidget")
        FilesWidget.resize(1229, 489)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FilesWidget.sizePolicy().hasHeightForWidth())
        FilesWidget.setSizePolicy(sizePolicy)
        FilesWidget.setStyleSheet("#button_import_folder, #button_import_files, #button_create_folder {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #0092FF;\n"
"}\n"
"\n"
"#button_back {\n"
"    background-color: #FFFFFF;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"#button_back:hover {\n"
"    background-color: #FBFBFB;\n"
"}\n"
"\n"
"#line_edit_current_directory {\n"
"    background-color: none;\n"
"    border: none;\n"
"}\n"
"\n"
"#button_import_folder:hover, #button_import_files:hover, #button_create_folder:hover {\n"
"    color: #0070DD;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    margin-top: 48px;\n"
"}\n"
"\n"
"#badge_widget {\n"
"    background-color: #0092FF;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#label_role {\n"
"    color: #FFFFFF;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(FilesWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_files = QtWidgets.QWidget(FilesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_files.sizePolicy().hasHeightForWidth())
        self.widget_files.setSizePolicy(sizePolicy)
        self.widget_files.setObjectName("widget_files")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_files)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_back = Button(self.widget_files)
        self.button_back.setMinimumSize(QtCore.QSize(38, 38))
        self.button_back.setMaximumSize(QtCore.QSize(38, 38))
        self.button_back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/arrow_back.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_back.setIcon(icon)
        self.button_back.setIconSize(QtCore.QSize(24, 24))
        self.button_back.setFlat(True)
        self.button_back.setProperty("color", QtGui.QColor(136, 138, 133))
        self.button_back.setObjectName("button_back")
        self.horizontalLayout_2.addWidget(self.button_back)
        self.line_edit_search = QtWidgets.QLineEdit(self.widget_files)
        self.line_edit_search.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout_2.addWidget(self.line_edit_search)
        self.button_create_folder = Button(self.widget_files)
        self.button_create_folder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/material/create_new_folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_create_folder.setIcon(icon1)
        self.button_create_folder.setIconSize(QtCore.QSize(24, 24))
        self.button_create_folder.setFlat(True)
        self.button_create_folder.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_create_folder.setObjectName("button_create_folder")
        self.horizontalLayout_2.addWidget(self.button_create_folder)
        self.button_import_files = Button(self.widget_files)
        self.button_import_files.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/images/material/control_point.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_import_files.setIcon(icon2)
        self.button_import_files.setIconSize(QtCore.QSize(24, 24))
        self.button_import_files.setFlat(True)
        self.button_import_files.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_import_files.setObjectName("button_import_files")
        self.horizontalLayout_2.addWidget(self.button_import_files)
        self.button_import_folder = Button(self.widget_files)
        self.button_import_folder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/images/material/add_circle_outline.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_import_folder.setIcon(icon3)
        self.button_import_folder.setIconSize(QtCore.QSize(24, 24))
        self.button_import_folder.setFlat(True)
        self.button_import_folder.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_import_folder.setObjectName("button_import_folder")
        self.horizontalLayout_2.addWidget(self.button_import_folder)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.badge_widget = QtWidgets.QWidget(self.widget_files)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.badge_widget.sizePolicy().hasHeightForWidth())
        self.badge_widget.setSizePolicy(sizePolicy)
        self.badge_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.badge_widget.setObjectName("badge_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.badge_widget)
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_role = QtWidgets.QLabel(self.badge_widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_role.setFont(font)
        self.label_role.setObjectName("label_role")
        self.horizontalLayout.addWidget(self.label_role)
        self.horizontalLayout_2.addWidget(self.badge_widget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.table_files_layout = QtWidgets.QGridLayout()
        self.table_files_layout.setContentsMargins(0, 10, 0, 0)
        self.table_files_layout.setObjectName("table_files_layout")
        self.table_files = FileTable(self.widget_files)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.table_files.setFont(font)
        self.table_files.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table_files.setFrameShadow(QtWidgets.QFrame.Plain)
        self.table_files.setLineWidth(0)
        self.table_files.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_files.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_files.setProperty("showDropIndicator", False)
        self.table_files.setDragEnabled(True)
        self.table_files.setDragDropOverwriteMode(False)
        self.table_files.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.table_files.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.table_files.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.table_files.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_files.setIconSize(QtCore.QSize(32, 32))
        self.table_files.setShowGrid(False)
        self.table_files.setGridStyle(QtCore.Qt.NoPen)
        self.table_files.setWordWrap(False)
        self.table_files.setCornerButtonEnabled(False)
        self.table_files.setColumnCount(5)
        self.table_files.setObjectName("table_files")
        self.table_files.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_files.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_files.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_files.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_files.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_files.setHorizontalHeaderItem(4, item)
        self.table_files.horizontalHeader().setVisible(True)
        self.table_files.horizontalHeader().setStretchLastSection(False)
        self.table_files.verticalHeader().setVisible(False)
        self.table_files.verticalHeader().setSortIndicatorShown(False)
        self.table_files.verticalHeader().setStretchLastSection(False)
        self.table_files_layout.addWidget(self.table_files, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.table_files_layout)
        self.verticalLayout.addWidget(self.widget_files)

        self.retranslateUi(FilesWidget)
        QtCore.QMetaObject.connectSlotsByName(FilesWidget)

    def retranslateUi(self, FilesWidget):
        _translate = QtCore.QCoreApplication.translate
        FilesWidget.setWindowTitle(_translate("FilesWidget", "Form"))
        self.button_back.setToolTip(_translate("FilesWidget", "TEXT_FILE_BACK_TO_WORKSPACES_TOOLTIP"))
        self.line_edit_search.setPlaceholderText(_translate("FilesWidget", "TEXT_FILE_FILTER_PLACEHOLDER"))
        self.button_create_folder.setToolTip(_translate("FilesWidget", "TEXT_FILE_CREATE_FOLDER_TOOLTIP"))
        self.button_create_folder.setText(_translate("FilesWidget", "ACTION_FILE_CREATE_FOLDER"))
        self.button_import_files.setToolTip(_translate("FilesWidget", "TEXT_FILE_IMPORT_FILES_TOOLTIP"))
        self.button_import_files.setText(_translate("FilesWidget", "ACTION_FILE_IMPORT_FILES"))
        self.button_import_folder.setToolTip(_translate("FilesWidget", "TEXT_FILE_IMPORT_FOLDER_TOOLTIP"))
        self.button_import_folder.setText(_translate("FilesWidget", "ACTION_FILE_IMPORT_FOLDER"))
        self.table_files.setSortingEnabled(True)
        item = self.table_files.horizontalHeaderItem(1)
        item.setText(_translate("FilesWidget", "TEXT_FILE_NAME_HEADER"))
        item = self.table_files.horizontalHeaderItem(2)
        item.setText(_translate("FilesWidget", "TEXT_FILE_CREATED_HEADER"))
        item = self.table_files.horizontalHeaderItem(3)
        item.setText(_translate("FilesWidget", "TEXT_FILE_UPDATED_HEADER"))
        item = self.table_files.horizontalHeaderItem(4)
        item.setText(_translate("FilesWidget", "TEXT_FILE_SIZE_HEADER"))
from parsec.core.gui.custom_widgets import Button
from parsec.core.gui.file_table import FileTable
from parsec.core.gui import resources_rc
