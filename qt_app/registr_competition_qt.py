from PyQt5 import QtWidgets
from design.py.registration_competition_form import Ui_RegistrCompetitions


class RegistrCompetitionsQt(QtWidgets.QDialog, Ui_RegistrCompetitions):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
