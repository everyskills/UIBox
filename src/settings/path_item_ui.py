# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'path_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets

class KUi_Form(QtWidgets.QWidget):
    def __init__(self):
        super(KUi_Form, self).__init__()
        self.setObjectName("self")
        self.resize(476, 49)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_icon = QtWidgets.QToolButton(self)
        self.btn_icon.setText("")
        self.btn_icon.setIconSize(QtCore.QSize(25, 25))
        self.btn_icon.setAutoRaise(True)
        self.btn_icon.setObjectName("btn_icon")
        self.btn_icon.setStyleSheet("background: none; border: none;")
        self.gridLayout.addWidget(self.btn_icon, 0, 0, 1, 1)
        self.line_path = QtWidgets.QLineEdit(self)
        self.line_path.setStyleSheet("padding: 7px;\n"
"border-radius: 5px;")
        self.line_path.setFrame(False)
        self.line_path.setObjectName("line_path")
        self.gridLayout.addWidget(self.line_path, 0, 1, 1, 1)
        self.btn_browser = QtWidgets.QToolButton(self)
        self.btn_browser.setText("")
        self.btn_browser.setIconSize(QtCore.QSize(25, 25))
        self.btn_browser.setAutoRaise(True)
        self.btn_browser.setObjectName("btn_browser")
        self.gridLayout.addWidget(self.btn_browser, 0, 2, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.line_path.setPlaceholderText(_translate("self", "path to include"))