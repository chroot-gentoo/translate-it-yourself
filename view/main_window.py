# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

from view.ui_views.mainWindow import Ui_MainWindow
from view.ui_views.info_boxes import MessageBoxes
from view.ui_views.create_project_dialog import CreateProjectDialogWindow
from view.ui_views.open_project_dialog import OpenProjectDialogWindow
from view.ui_views.delete_project_dialog import DeleteProjectDialogWindow

from view.translate_api import translate

AUTO_SAVE_TIMEOUT = 1000 * 60 * 5


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """ Главное окно.
        Ui_MainWindow - форма для setupUi"""
    _current_block = None
    _project_changed = False  # при нажатии на save или auto-save меняется на False
    _set_of_changed_blocks = set()

    open_cur_project = QtCore.pyqtSignal(str)
    load_from_file = QtCore.pyqtSignal(str)
    set_text_blocks = QtCore.pyqtSignal(dict)
    dump_to_file = QtCore.pyqtSignal(list, str)
    create_project = QtCore.pyqtSignal(dict)
    delete_project = QtCore.pyqtSignal(str)
    get_projects_names = QtCore.pyqtSignal(str)  # передаем параметром действие - создание или удаление проекта

    def __init__(self, paren=None):
        QtWidgets.QMainWindow.__init__(self, paren)
        self.setupUi(self)
        self.info_box = MessageBoxes(self)

        # Таймер автосохранения, по истичению запускает метод _save_project, длительность задает AUTO_SAVE_TIMEOUT
        self.autosave_timer = QtCore.QTimer(self)
        self.autosave_timer.setTimerType(QtCore.Qt.VeryCoarseTimer)
        self.autosave_timer.start(AUTO_SAVE_TIMEOUT)
        self.autosave_timer.timeout.connect(self.auto_save)

        self.originalListWidget.itemClicked.connect(self.original_list_click)
        self.translatedListWidget.itemClicked.connect(self.translated_list_click)

        self.originalListWidget.verticalScrollBar().valueChanged.connect(self.sync_translated_scroll)
        self.translatedListWidget.verticalScrollBar().valueChanged.connect(self.sync_original_scroll)

        self.workWithBlockPushButton.clicked.connect(self.work_with_block)
        self.originalListWidget.itemDoubleClicked.connect(lambda: self.work_with_block(on_d_click=True))
        self.translatedListWidget.itemDoubleClicked.connect(self.work_with_block)

        self.saveBlockPushButton.clicked.connect(self.save_block)
        self.translateApiPushButton.clicked.connect(self.translate_word)

        self.createTrigger.triggered.connect(self.create_new_project)
        self.openTrigger.triggered.connect(self.open_project_triggered)
        self.deleteTrigger.triggered.connect(self.delete_project_triggered)
        self.exportTxtTrigger.triggered.connect(self.export_txt)
        self.exitToolButton.clicked.connect(self.close)
        self.saveToolButton.clicked.connect(self.auto_save)
        self.saveTrigger.triggered.connect(self.auto_save)
        self.exitTrigger.triggered.connect(self.close)

    def sync_translated_scroll(self, value):
        self.translatedListWidget.verticalScrollBar().setValue(value)

    def sync_original_scroll(self, value):
        self.originalListWidget.verticalScrollBar().setValue(value)

    # TODO: добавить сохранение при смене блока без нажатия кнопки "сохранить"/либо сделать кнопку перевести неактивной
    def work_with_block(self, on_d_click=False):
        """ Начать работу над переводом выделенного блока текста, срабатывает при нажатии кнопки 'перевести блок'. """
        if on_d_click and self._current_block:
            self.save_block()
        self._current_block = self.translatedListWidget.currentRow()
        self.translatedPartStackedWidget.setCurrentWidget(self.editorPage)
        self.originalTextEdit.setPlainText(self.originalListWidget.currentItem().text())
        self.translatedTextEdit.setPlainText(self.translatedListWidget.currentItem().text())
        self.workWithBlockPushButton.setEnabled(False)
        # self.translatedTextEdit.setFocus()

    def save_block(self):
        """ Сохранение измененного текста блока в item. Срабатывает при нажатии кнопки 'Сохранить блок'. """
        self.translatedListWidget.item(self._current_block).setText(self.translatedTextEdit.toPlainText())
        self.translatedPartStackedWidget.setCurrentWidget(self.listPage)
        self.workWithBlockPushButton.setEnabled(True)
        self._project_changed = True
        self._set_of_changed_blocks.add(self._current_block)
        self._current_block = None

    def add_text(self, list_of_tuples):
        for o, t in list_of_tuples:
            orig_item = QtWidgets.QListWidgetItem(o, self.originalListWidget)
            trans_item = QtWidgets.QListWidgetItem(t, self.translatedListWidget)
            self.originalListWidget.addItem(orig_item)
            self.translatedListWidget.addItem(trans_item)
        self.align_text_blocks_height()

    # TODO: когда будет выгрузка текста из базы - переработать под больший размер
    def align_text_blocks_height(self):
        """ Выравнивает высоту блоков текста по тексту оригинала, срабатывает при изменении размера окна"""
        for string_index in range(self.translatedListWidget.count()):
            orig_index = self.originalListWidget.model().index(string_index)
            orig_height = self.originalListWidget.visualRect(orig_index).height()
            self.translatedListWidget.item(string_index).setSizeHint(QtCore.QSize(-1, orig_height))

    @QtCore.pyqtSlot()
    def original_list_click(self):
        """ Синхронизирует выделение блоков текста по клику на блок"""
        self.translatedListWidget.setCurrentRow(self.originalListWidget.currentRow())

    def translated_list_click(self):
        """ Синхронизирует выделение блоков текста по клику на блок"""
        self.originalListWidget.setCurrentRow(self.translatedListWidget.currentRow())

    def translate_word(self):
        _PATTERN = 'оригинал: {} \n перевод: {}'
        text = self.originalTextEdit.createMimeDataFromSelection().text()
        if text:
            type_, desc_, text_ = translate(text)
            if type_ == 'info':
                self.info_box(type_, desc_, _PATTERN.format(text, text_))
                QtWidgets.QApplication.clipboard().setText(text_)
            else:
                self.info_box(type_, desc_, text_)

    def export_txt(self):
        """
        Метод экспорта в TXT
        :return: list перевода и path для сохранения
        """
        file = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption='Экспортировать', filter='All (*);;TXT (*.txt)', initialFilter='TXT (*.txt)'
        )
        if file[0]:
            text = [self.translatedListWidget.item(i).text() for i in range(self.translatedListWidget.count())]
            self.dump_to_file.emit(text, file[0])

    # TODO: при проверке имени проекта, если такое уже есть (сигнал?) снова запускать эту функцию и окно с ошибкой
    @QtCore.pyqtSlot()
    def create_new_project(self):
        """ Запуск диалогового окна создания нового проекта,
        при нажатии на "Создать" генерируется сигнял new_project с информацией из полей.
        """
        if self.close_current_project():
            create_project_dialog = CreateProjectDialogWindow(self)
            create_project_dialog.show()

    # TODO: полагаю имя проекта передавать надо не сюда, оно предается сингалом
    @QtCore.pyqtSlot()
    def open_project_triggered(self):
        if self.close_current_project():
            self.get_projects_names.emit('open')

    def open_projects(self, projects):
        print(projects)
        open_project_dialog = OpenProjectDialogWindow(self)
        open_project_dialog.add_projects_list(projects)
        open_project_dialog.show()

    def delete_project_triggered(self):
        self.get_projects_names.emit('delete')

    def delete_projects(self, projects):
        delete_project_dialog = DeleteProjectDialogWindow(self)
        delete_project_dialog.add_projects_list(projects)
        delete_project_dialog.show()

    def resizeEvent(self, event):
        """ Переопределение метода изменения размера окна,
            запускает выравниевание высоты блоков при событии изменения окна"""
        event.accept()
        self.align_text_blocks_height()

    def closeEvent(self, event):
        if self.close_current_project():
            event.accept()
        else:
            event.ignore()

    def close_current_project(self):
        if self._project_changed:
            answ = self.info_box('question', 'Закрытие проекта', 'Сохранить изменения?')
            if answ == QtWidgets.QMessageBox.Cancel:
                return False

            elif answ == QtWidgets.QMessageBox.Yes:
                self.save_project()
                self.clear_project()
                return True

            elif answ == QtWidgets.QMessageBox.No:
                self.clear_project()
                return True
        self.clear_project()
        return True

    def clear_project(self):
        self.originalListWidget.clear()
        self.translatedListWidget.clear()

    def showEvent(self, event):
        self.align_text_blocks_height()
        event.accept()

    def auto_save(self):
        if self._project_changed:
            self.save_project()

    def save_project(self):
        changes_dict = {}
        if self._set_of_changed_blocks:
            for i in self._set_of_changed_blocks:
                changes_dict[i] = (self.originalListWidget.item(i).text(), self.translatedListWidget.item(i).text())
            self.set_text_blocks.emit(changes_dict)
            self._project_changed = False
            self._set_of_changed_blocks.clear()

        elif not self._project_changed:
            for i in range(self.translatedListWidget.count()):
                changes_dict[i] = (self.originalListWidget.item(i).text(), self.translatedListWidget.item(i).text())
            self.set_text_blocks.emit(changes_dict)
            self._project_changed = False

import sys
sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
