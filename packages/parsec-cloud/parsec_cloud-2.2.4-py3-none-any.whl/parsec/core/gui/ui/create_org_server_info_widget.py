# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/create_org_server_info_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateOrgServerInfoWidget(object):
    def setupUi(self, CreateOrgServerInfoWidget):
        CreateOrgServerInfoWidget.setObjectName("CreateOrgServerInfoWidget")
        CreateOrgServerInfoWidget.resize(463, 216)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateOrgServerInfoWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CreateOrgServerInfoWidget)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.check_use_custom = QtWidgets.QCheckBox(CreateOrgServerInfoWidget)
        self.check_use_custom.setObjectName("check_use_custom")
        self.verticalLayout.addWidget(self.check_use_custom)
        self.label_2 = QtWidgets.QLabel(CreateOrgServerInfoWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_custom_server = QtWidgets.QWidget(CreateOrgServerInfoWidget)
        self.widget_custom_server.setObjectName("widget_custom_server")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_custom_server)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.widget_custom_server)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_10.addWidget(self.label_8)
        self.line_edit_server_addr = QtWidgets.QLineEdit(self.widget_custom_server)
        self.line_edit_server_addr.setObjectName("line_edit_server_addr")
        self.verticalLayout_10.addWidget(self.line_edit_server_addr)
        self.verticalLayout_2.addLayout(self.verticalLayout_10)
        self.verticalLayout.addWidget(self.widget_custom_server)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(CreateOrgServerInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateOrgServerInfoWidget)

    def retranslateUi(self, CreateOrgServerInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateOrgServerInfoWidget.setWindowTitle(_translate("CreateOrgServerInfoWidget", "Form"))
        self.label.setText(_translate("CreateOrgServerInfoWidget", "TEXT_CREATE_ORG_DEFAULT_SERVER"))
        self.check_use_custom.setText(_translate("CreateOrgServerInfoWidget", "TEXT_CREATE_ORG_USER_CUSTOM_SERVER"))
        self.label_2.setText(_translate("CreateOrgServerInfoWidget", "TEXT_LABEL_CUSTOM_SERVER_NEED_SPONTANEOUS"))
        self.label_8.setText(_translate("CreateOrgServerInfoWidget", "TEXT_LABEL_SERVER_ADDRESS"))
        self.line_edit_server_addr.setPlaceholderText(_translate("CreateOrgServerInfoWidget", "TEXT_LABEL_SERVER_ADDRESS_PLACEHOLDER"))
