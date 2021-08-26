import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from loguru import logger

from app import AutoRequestArrayCompetition
from design.py.registration_competition_form import Ui_RegistrCompetitions
from settings import PATH_TO_LOG

PATH_TO_LOG_COMPETITION = PATH_TO_LOG + 'log_competition.txt'



class CompetitionWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, path_to_file_accounts: str, path_to_file_competition: str, change_vpn=5, repeat=2):
        super().__init__()
        self.path_to_file_accounts = path_to_file_accounts
        self.path_to_file_competition = path_to_file_competition
        self.change_vpn = change_vpn
        self.repeat = repeat

    def run(self):
        """Long-running task."""
        try:
            c = AutoRequestArrayCompetition()
            c.request_many_competition(path_to_file_accounts=self.path_to_file_accounts,
                                       path_to_file_competition=self.path_to_file_competition,
                                       change_vpn=self.change_vpn,
                                       repeat=self.repeat)
        except Exception:
            logger.exception("What?!")
        self.finished.emit()


class RegistrCompetitionsQt(QtWidgets.QDialog, Ui_RegistrCompetitions):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        logger.add(PATH_TO_LOG_COMPETITION, format='{time} {level} {message}')
        self.pushButton.clicked.connect(lambda: self.browse_file(button=self.pushButton))
        self.pushButton_3.clicked.connect(lambda: self.browse_file(button=self.pushButton_3))
        self.pushButton_2.clicked.connect(self.start_registr_competition)
        self.pushButton_4.clicked.connect(self.stop_thread)
        self.commandLinkButton.clicked.connect(self.open_file)
        self.textBrowser.append(open(PATH_TO_LOG_COMPETITION).read())

    def browse_file(self, button: QtWidgets.QPushButton):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", filter="*.csv")
        if file:
            button.setText(file[0])

    @staticmethod
    def clear_log():
        f = open(PATH_TO_LOG_COMPETITION, 'w')
        f.close()

    @staticmethod
    def open_file():
        file_name = AutoRequestArrayCompetition.file_output
        os.startfile(file_name)

    def stop_thread(self):
        self.thread().exit()

    def update_log_field(self):
        text = open(PATH_TO_LOG_COMPETITION).read()
        self.textBrowser.clear()
        self.textBrowser.append(text)

    def start_registr_competition(self):
        self.clear_log()

        self.background_thread = QThread()
        self.worker = CompetitionWorker(path_to_file_accounts=str(self.pushButton.text()),
                                        path_to_file_competition=str(self.pushButton_3.text()),
                                        change_vpn=int(self.spinBox_2.value()),
                                        repeat=int(self.spinBox.value()))
        self.worker.moveToThread(self.background_thread)
        self.background_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.background_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.background_thread.finished.connect(self.background_thread.deleteLater)
        self.background_thread.start()

        self.pushButton_2.setEnabled(False)
        self.background_thread.finished.connect(
            lambda: self.pushButton_2.setEnabled(True)
        )
        self.background_thread.finished.connect(
            lambda: self.update_log_field()
        )

def main():
    while True:
        app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
        window = RegistrCompetitionsQt()  # Создаём объект класса ExampleApp
        window.show()  # Показываем окно
        sys.exit(app.exec_())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
