import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

from design.py.main_window_form import Ui_MainWindow
from qt_views.registr_accounts_qt import RegistAccountsQt
from qt_views.registr_competition_qt import RegistrCompetitionsQt


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.button_registr_accounts.clicked.connect(self.registr_accounts_click)
        self.button_registr_competitions.clicked.connect(self.registr_competitions_click)

    def registr_accounts_click(self):
        dlg = RegistAccountsQt()
        dlg.exec()

    def registr_competitions_click(self):
        dlg = RegistrCompetitionsQt()
        dlg.exec()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
