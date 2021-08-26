import os
import sys
import time
import threading
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from loguru import logger
from PyQt5 import QtWidgets
from app import AutoRegistrationArrayAccount
from design.py.registration_account_form import Ui_RegistrAccounts
from settings import PATH_TO_LOG

PATH_TO_LOG_REGISTR = PATH_TO_LOG + 'log_registration.txt'



class RegistrationWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, path_to_file_accounts: str, change_vpn=5, repeat=2):
        super().__init__()
        self.path_to_file_accounts = path_to_file_accounts
        self.change_vpn = change_vpn
        self.repeat = repeat

    def run(self):
        """Long-running task."""
        try:
            c = AutoRegistrationArrayAccount()
            c.registration_many_accounts(path_to_file_accounts=self.path_to_file_accounts,
                                         change_vpn=self.change_vpn,
                                         repeat=self.repeat)
        except Exception:
            logger.exception("What?!")
        self.finished.emit()


class RegistAccountsQt(QtWidgets.QDialog, Ui_RegistrAccounts):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        logger.add(PATH_TO_LOG_REGISTR, format='{time} {level} {message}')
        self.pushButton.clicked.connect(self.browse_file)
        self.pushButton_2.clicked.connect(self.start_registr_accounts)
        self.pushButton_3.clicked.connect(self.stop_thread)
        self.commandLinkButton.clicked.connect(self.open_file)
        self.textBrowser.append(open(PATH_TO_LOG_REGISTR).read())

    def browse_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", filter="*.csv")
        if file:
            self.pushButton.setText(file[0])

    @staticmethod
    def clear_log():
        f = open(PATH_TO_LOG_REGISTR, 'w')
        f.close()

    @staticmethod
    def open_file():
        file_name = AutoRegistrationArrayAccount.file_output
        os.startfile(file_name)

    def stop_thread(self):
        self.thread().exit()

    def update_log_field(self):
        text = open(PATH_TO_LOG_REGISTR).read()
        self.textBrowser.clear()
        self.textBrowser.append(text)

    def start_registr_accounts(self):
        self.clear_log()
        self.background_thread = QThread()
        self.worker = RegistrationWorker(path_to_file_accounts=str(self.pushButton.text()),
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
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = RegistAccountsQt()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
