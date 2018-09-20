from PyQt5 import QtGui, QtCore, QtWidgets

class MessageBoxes:
    # TODO: добавить в методы возможность изменять кнопки (example: info пароль слишком короткий: изменить, продолжить)
    def __init__(self, parent=None):
        self.question_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, 'are you sure?', '???',
                                                  buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No |
                                                          QtWidgets.QMessageBox.Cancel,  parent=parent)
        self.warning_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'oops', '!!!',
                                                 buttons=QtWidgets.QMessageBox.Ok, parent=parent)
        self.error_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, 'auch', '!!!',
                                               buttons=QtWidgets.QMessageBox.Ok, parent=parent)
        self.info_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'info', 'info',
                                              buttons=QtWidgets.QMessageBox.Ok, parent=parent)

    def make_question_box(self, title, text):
        self.question_box.setWindowTitle(title)
        self.question_box.setText(text)
        return self.question_box.exec()

    def make_warning_box(self, title, text):
        self.warning_box.setWindowTitle(title)
        self.warning_box.setText(text)
        self.warning_box.exec()

    def make_error_box(self, title, text):
        self.error_box.setWindowTitle(title)
        self.error_box.setText(text)
        self.error_box.exec()

    def make_info_box(self, title, text):
        self.info_box.setWindowTitle(title)
        self.info_box.setText(text)
        self.info_box.exec()

    def __call__(self, box_type, title, text):
        if box_type == 'question':
            return self.make_question_box(title, text)
        elif box_type == 'warning':
            return self.make_warning_box(title, text)
        elif box_type == 'error':
            return self.make_error_box(title, text)
        elif box_type == 'info':
            return self.make_info_box(title, text)
