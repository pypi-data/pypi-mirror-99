# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/changelog_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChangelogWidget(object):
    def setupUi(self, ChangelogWidget):
        ChangelogWidget.setObjectName("ChangelogWidget")
        ChangelogWidget.resize(500, 400)
        ChangelogWidget.setMinimumSize(QtCore.QSize(500, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(ChangelogWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_changelog = QtWidgets.QTextBrowser(ChangelogWidget)
        self.text_changelog.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.text_changelog.setFrameShadow(QtWidgets.QFrame.Plain)
        self.text_changelog.setLineWidth(0)
        self.text_changelog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_changelog.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)
        self.text_changelog.setOpenExternalLinks(True)
        self.text_changelog.setObjectName("text_changelog")
        self.verticalLayout.addWidget(self.text_changelog)

        self.retranslateUi(ChangelogWidget)
        QtCore.QMetaObject.connectSlotsByName(ChangelogWidget)

    def retranslateUi(self, ChangelogWidget):
        _translate = QtCore.QCoreApplication.translate
        ChangelogWidget.setWindowTitle(_translate("ChangelogWidget", "Form"))
