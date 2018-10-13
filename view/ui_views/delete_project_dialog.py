from PyQt5 import QtWidgets, QtCore, QtGui

from view.ui_views.deleteProjectWindow import Ui_Dialog


class DeleteProjectDialogWindow(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cancelPushButton.clicked.connect(self.close)
        self.deletePushButton.clicked.connect(self.delete_project_clicked)
        self.deleteProjectListWidget.itemDoubleClicked.connect(self.delete_project_clicked)

    def delete_project_clicked(self):
        project_item = self.deleteProjectListWidget.currentItem()
        if project_item:
            project_name = project_item.text()
            self.parent().delete_project.emit(project_name)
            self.close()
        else:
            self.parent().info_box('info', 'Не выбран проект', 'Выберите проект')

    def add_projects_list(self, projects):
        self.deleteProjectListWidget.addItems(projects)
