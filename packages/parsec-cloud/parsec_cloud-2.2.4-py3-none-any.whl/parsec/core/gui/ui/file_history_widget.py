# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/file_history_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileHistoryWidget(object):
    def setupUi(self, FileHistoryWidget):
        FileHistoryWidget.setObjectName("FileHistoryWidget")
        FileHistoryWidget.resize(570, 441)
        self.verticalLayout = QtWidgets.QVBoxLayout(FileHistoryWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setContentsMargins(-1, 0, -1, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setObjectName("vertical_layout")
        self.area_list = QtWidgets.QScrollArea(FileHistoryWidget)
        self.area_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.area_list.setFrameShadow(QtWidgets.QFrame.Plain)
        self.area_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.area_list.setWidgetResizable(True)
        self.area_list.setObjectName("area_list")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 568, 390))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.layout_history = QtWidgets.QVBoxLayout()
        self.layout_history.setObjectName("layout_history")
        self.verticalLayout_4.addLayout(self.layout_history)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.area_list.setWidget(self.scrollAreaWidgetContents)
        self.vertical_layout.addWidget(self.area_list)
        self.spinner_frame = QtWidgets.QFrame(FileHistoryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinner_frame.sizePolicy().hasHeightForWidth())
        self.spinner_frame.setSizePolicy(sizePolicy)
        self.spinner_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.spinner_frame.setObjectName("spinner_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.spinner_frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.spinner = SpinnerWidget(self.spinner_frame)
        self.spinner.setObjectName("spinner")
        self.horizontalLayout_4.addWidget(self.spinner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.vertical_layout.addWidget(self.spinner_frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_load_more_entries = QtWidgets.QPushButton(FileHistoryWidget)
        self.button_load_more_entries.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_load_more_entries.setObjectName("button_load_more_entries")
        self.horizontalLayout.addWidget(self.button_load_more_entries)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.vertical_layout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.vertical_layout)

        self.retranslateUi(FileHistoryWidget)
        QtCore.QMetaObject.connectSlotsByName(FileHistoryWidget)

    def retranslateUi(self, FileHistoryWidget):
        _translate = QtCore.QCoreApplication.translate
        FileHistoryWidget.setWindowTitle(_translate("FileHistoryWidget", "Form"))
        self.button_load_more_entries.setText(_translate("FileHistoryWidget", "ACTION_FILE_HISTORY_LOAD_MORE_ENTRIES"))
from parsec.core.gui.custom_widgets import SpinnerWidget
