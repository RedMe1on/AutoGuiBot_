from PyQt5 import QtWidgets
from design.py.registration_account_form import Ui_RegistrAccounts


class RegistAccountsQt(QtWidgets.QDialog, Ui_RegistrAccounts):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def browse_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", filter="*.csv")
        print(file)
        if file:
            self.pushButton.setText(file[0])
        print(self.pushButton.text())

        c = AutoRegistrationArrayAccount()
        d = c.db_class.read_file(file[0])
        print(d)
