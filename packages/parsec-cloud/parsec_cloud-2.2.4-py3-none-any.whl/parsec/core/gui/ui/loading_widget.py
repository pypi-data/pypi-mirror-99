# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/loading_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadingWidget(object):
    def setupUi(self, LoadingWidget):
        LoadingWidget.setObjectName("LoadingWidget")
        LoadingWidget.resize(400, 81)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadingWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_status = QtWidgets.QLabel(LoadingWidget)
        self.label_status.setObjectName("label_status")
        self.horizontalLayout.addWidget(self.label_status)
        self.label = QtWidgets.QLabel(LoadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progress_bar = QtWidgets.QProgressBar(LoadingWidget)
        self.progress_bar.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progress_bar.setFont(font)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout.addWidget(self.progress_bar)

        self.retranslateUi(LoadingWidget)
        QtCore.QMetaObject.connectSlotsByName(LoadingWidget)

    def retranslateUi(self, LoadingWidget):
        _translate = QtCore.QCoreApplication.translate
        LoadingWidget.setWindowTitle(_translate("LoadingWidget", "Form"))
        self.label_status.setText(_translate("LoadingWidget", "TEXT_IMPORT_FILES_PROGRESS"))
