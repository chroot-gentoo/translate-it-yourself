# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openProjectWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 510)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.openProjectListWidget = QtWidgets.QListWidget(Dialog)
        self.openProjectListWidget.setObjectName("openProjectListWidget")
        self.gridLayout.addWidget(self.openProjectListWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.openPushButton = QtWidgets.QPushButton(Dialog)
        self.openPushButton.setObjectName("openPushButton")
        self.horizontalLayout.addWidget(self.openPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(Dialog)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.openPushButton.setText(_translate("Dialog", "Открыть"))
        self.cancelPushButton.setText(_translate("Dialog", "Отмена"))

