# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/keys_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KeysWidget(object):
    def setupUi(self, KeysWidget):
        KeysWidget.setObjectName("KeysWidget")
        KeysWidget.resize(474, 468)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(KeysWidget.sizePolicy().hasHeightForWidth())
        KeysWidget.setSizePolicy(sizePolicy)
        KeysWidget.setStyleSheet("#scroll_content {\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#keys_widget, #scrollArea {\n"
"    background-color: #F4F4F4;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(KeysWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_import_key = Button(KeysWidget)
        self.button_import_key.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_import_key.setIconSize(QtCore.QSize(24, 24))
        self.button_import_key.setFlat(True)
        self.button_import_key.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_import_key.setObjectName("button_import_key")
        self.horizontalLayout.addWidget(self.button_import_key)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.keys_widget = QtWidgets.QWidget(KeysWidget)
        self.keys_widget.setMinimumSize(QtCore.QSize(400, 250))
        self.keys_widget.setObjectName("keys_widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.keys_widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.keys_widget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_content.setGeometry(QtCore.QRect(0, 0, 474, 426))
        self.scroll_content.setObjectName("scroll_content")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scroll_content)
        self.verticalLayout_3.setContentsMargins(20, 10, 20, 10)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scroll_content)
        self.verticalLayout_5.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.keys_widget)

        self.retranslateUi(KeysWidget)
        QtCore.QMetaObject.connectSlotsByName(KeysWidget)

    def retranslateUi(self, KeysWidget):
        _translate = QtCore.QCoreApplication.translate
        self.button_import_key.setToolTip(_translate("KeysWidget", "TEXT_IMPORT_KEY_TOOLTIP"))
        self.button_import_key.setText(_translate("KeysWidget", "ACTION_IMPORT_KEY"))
from parsec.core.gui.custom_widgets import Button
