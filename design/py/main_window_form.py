# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(399, 154)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.button_registr_competitions = QtWidgets.QPushButton(self.centralwidget)
        self.button_registr_competitions.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.button_registr_competitions, 1, 0, 1, 1)
        self.button_registr_accounts = QtWidgets.QPushButton(self.centralwidget)
        self.button_registr_accounts.setEnabled(True)
        self.button_registr_accounts.setMaximumSize(QtCore.QSize(299, 23))
        self.button_registr_accounts.setObjectName("pushButton")
        self.gridLayout.addWidget(self.button_registr_accounts, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_registr_competitions.setText(_translate("MainWindow", "Регистрация на конкурсы"))
        self.button_registr_accounts.setText(_translate("MainWindow", "Регистрация аккаунтов"))