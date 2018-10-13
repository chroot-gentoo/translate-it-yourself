from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 510)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.deleteProjectListWidget = QtWidgets.QListWidget(Dialog)
        self.deleteProjectListWidget.setObjectName("deleteProjectListWidget")
        self.gridLayout.addWidget(self.deleteProjectListWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.deletePushButton = QtWidgets.QPushButton(Dialog)
        self.deletePushButton.setObjectName("deletePushButton")
        self.horizontalLayout.addWidget(self.deletePushButton)
        self.cancelPushButton = QtWidgets.QPushButton(Dialog)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.deletePushButton.setText(_translate("Dialog", "Удалить"))
        self.cancelPushButton.setText(_translate("Dialog", "Отмена"))
