from PyQt5 import QtWidgets, QtCore, QtGui

from view.ui_views.openProjectWindow import Ui_Dialog


class OpenProjectDialogWindow(QtWidgets.QDialog, Ui_Dialog):
    # сигнал будет передавать ?имя? проекта... достаточно ли строки?
    opent_project_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cancelPushButton.clicked.connect(self.close)
        self.openPushButton.clicked.connect(self.open_project_clicked)
        self.openProjectListWidget.itemDoubleClicked.connect(self.open_project_clicked)

    def open_project_clicked(self):
        project_item = self.openProjectListWidget.currentItem()
        if project_item:
            project_name = project_item.text()
            self.opent_project_signal.emit(project_name)
            self.close()
        else:
            self.parent().info_box('info', 'Не выбран проект', 'Выберите проект')
