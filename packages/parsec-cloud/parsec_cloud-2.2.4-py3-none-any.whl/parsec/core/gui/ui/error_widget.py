# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/error_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ErrorWidget(object):
    def setupUi(self, ErrorWidget):
        ErrorWidget.setObjectName("ErrorWidget")
        ErrorWidget.resize(600, 283)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ErrorWidget.sizePolicy().hasHeightForWidth())
        ErrorWidget.setSizePolicy(sizePolicy)
        ErrorWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        ErrorWidget.setFont(font)
        ErrorWidget.setStyleSheet("QWidget#MessageWidget\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#line\n"
"{\n"
"color: #EEEEEE;\n"
"}\n"
"\n"
"#button_copy, #button_details\n"
"{\n"
"color: #999999;\n"
"border: none;\n"
"background-color: none;\n"
"}\n"
"\n"
"#text_details\n"
"{\n"
"color: #333333;\n"
"}\n"
"\n"
"#label_message\n"
"{\n"
"color: #F44336;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(ErrorWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_icon = IconLabel(ErrorWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_icon.sizePolicy().hasHeightForWidth())
        self.label_icon.setSizePolicy(sizePolicy)
        self.label_icon.setMinimumSize(QtCore.QSize(64, 64))
        self.label_icon.setMaximumSize(QtCore.QSize(64, 64))
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap(":/icons/images/material/error_outline.svg"))
        self.label_icon.setScaledContents(True)
        self.label_icon.setProperty("color", QtGui.QColor(244, 67, 54))
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout_2.addWidget(self.label_icon)
        self.label_message = QtWidgets.QLabel(ErrorWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_message.sizePolicy().hasHeightForWidth())
        self.label_message.setSizePolicy(sizePolicy)
        self.label_message.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_message.setFont(font)
        self.label_message.setText("")
        self.label_message.setTextFormat(QtCore.Qt.RichText)
        self.label_message.setWordWrap(True)
        self.label_message.setObjectName("label_message")
        self.horizontalLayout_2.addWidget(self.label_message)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(ErrorWidget)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_details = DropDownButton(ErrorWidget)
        self.button_details.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/arrow_drop_down.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_details.setIcon(icon)
        self.button_details.setIconSize(QtCore.QSize(24, 24))
        self.button_details.setCheckable(True)
        self.button_details.setChecked(False)
        self.button_details.setFlat(True)
        self.button_details.setProperty("color", QtGui.QColor(153, 153, 153))
        self.button_details.setObjectName("button_details")
        self.horizontalLayout_3.addWidget(self.button_details)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.button_copy = Button(ErrorWidget)
        self.button_copy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/material/assignment.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_copy.setIcon(icon1)
        self.button_copy.setIconSize(QtCore.QSize(24, 24))
        self.button_copy.setProperty("color", QtGui.QColor(153, 153, 153))
        self.button_copy.setObjectName("button_copy")
        self.horizontalLayout_3.addWidget(self.button_copy)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.text_details = QtWidgets.QTextEdit(ErrorWidget)
        self.text_details.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.text_details.setFrameShadow(QtWidgets.QFrame.Plain)
        self.text_details.setLineWidth(0)
        self.text_details.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_details.setObjectName("text_details")
        self.verticalLayout.addWidget(self.text_details)

        self.retranslateUi(ErrorWidget)
        QtCore.QMetaObject.connectSlotsByName(ErrorWidget)

    def retranslateUi(self, ErrorWidget):
        _translate = QtCore.QCoreApplication.translate
        ErrorWidget.setWindowTitle(_translate("ErrorWidget", "Form"))
        self.button_details.setToolTip(_translate("ErrorWidget", "TEXT_ERROR_SHOW_DETAILS_TOOLTIP"))
        self.button_details.setText(_translate("ErrorWidget", "ACTION_ERROR_SHOW_DETAILS"))
        self.button_copy.setToolTip(_translate("ErrorWidget", "TEXT_ERROR_COPY_TO_CLIPBOARD_TOOLTIP"))
        self.button_copy.setText(_translate("ErrorWidget", "ACTION_ERROR_COPY_DETAILS_TO_CLIPBOARD"))
        self.text_details.setHtml(_translate("ErrorWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
from parsec.core.gui.custom_widgets import Button, DropDownButton, IconLabel
from parsec.core.gui import resources_rc
