import sys

from PyQt5 import QtWidgets
from presenter.presenter import Presenter
from view.main_window import MainWindow
from model.model import Repository


def main():
    app = QtWidgets.QApplication(sys.argv)
    view = MainWindow()
    model = Repository()
    presenter = Presenter(view, model)
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()