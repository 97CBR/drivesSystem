# -*- coding: utf-8 -*-
# @Time    : 10/23/2019 5:35 PM
# @Author  : HR
# @File    : demo.py


from PyQt5 import QtCore, QtGui, QtWidgets
from storeUi.mainwindow import MainWindow
import sys

# import tensorflow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
