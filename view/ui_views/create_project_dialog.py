from PyQt5 import QtWidgets, QtCore
import sys

from view.ui_views.createProjectDialog import Ui_Dialog


class CreateProjectDialogWindow(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.filePathToolButton.clicked.connect(self.file_path_button)
        self.createPushButton.clicked.connect(self.create_button_clicked)
        self.cancelPushButton.clicked.connect(self.cancel_button_clicked)

    def create_button_clicked(self):
        self.drop_labels_color()
        project_name = self.projectNameLineEdit.text()
        author_name = self.authorNameLineEdit.text()
        source_link = self.sourceLinkLineEdit.text()
        file_path = self.filePathLineEdit.text()

        if self.check_fields(project_name, author_name):
            self.parent().create_project.emit({
                'project_name': project_name, 'author_name': author_name, 'source_link': source_link,
                'file_path': file_path
            })
            self.close()
        else:
            self.parent().info_box('info', 'заполните поля', 'заполните нехобходимые поля')

    def cancel_button_clicked(self):
        self.close()

    def file_path_button(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Новый проект', filter='All (*);;TXT (*.txt)', initialFilter='TXT (*.txt)'
        )
        self.filePathLineEdit.insert(file_path)

    def check_fields(self, proj_name, auth_name):
        not_filled = False
        if not proj_name:
            self.projectNameLabel.setStyleSheet('color: red')
            not_filled = True
        if not auth_name:
            self.authorNameLabel.setStyleSheet('color: red')
            not_filled = True

        if not_filled:
            return False
        return True

    def drop_labels_color(self):
        self.projectNameLabel.setStyleSheet('color: black')
        self.authorNameLabel.setStyleSheet('color: black')
        self.sourceLinkLabel.setStyleSheet('color: black')
        self.filePathLabel.setStyleSheet('color: black')
