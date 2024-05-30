# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myagv_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 레이아웃 설정
        self.layout = QVBoxLayout()
        self.centralwidget.setLayout(self.layout)

        # 카메라 화면을 위한 QLabel 추가
        self.camera_label = QLabel(self.centralwidget)
        self.layout.addWidget(self.camera_label)

        # Set font
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.font.setWeight(75)

        # Adface start button
        self.adaface_button = QtWidgets.QPushButton(self.centralwidget)
        self.adaface_button.setGeometry(QtCore.QRect(30, 50, 211, 41))
        self.adaface_button.setFont(self.font)
        self.adaface_button.setStyleSheet("QPushButton:pressed{\n"
                                          "   background-color:#c7c7d0;\n"
                                          "}\n"
                                          "")
        self.adaface_button.setObjectName("adaface_button")
        self.layout.addWidget(self.adaface_button)

        # Target person label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 211, 41))
        self.label.setFont(self.font)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)

        # Person select comboBox
        self.person_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.person_comboBox.setGeometry(QtCore.QRect(270, 50, 171, 41))
        self.person_comboBox.setFont(self.font)
        self.person_comboBox.setObjectName("person_comboBox")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        self.layout.addWidget(self.person_comboBox)

        # Person reset button
        self.person_button = QtWidgets.QPushButton(self.centralwidget)
        self.person_button.setGeometry(QtCore.QRect(450, 50, 101, 41))
        self.person_button.setFont(self.font)
        self.person_button.setStyleSheet("QPushButton:pressed{\n"
                                         "   background-color:#c7c7d0;\n"
                                         "}\n"
                                         "")
        self.person_button.setObjectName("person_button")
        self.layout.addWidget(self.person_button)

        # Log label
        self.label_log = QtWidgets.QLabel(self.centralwidget)
        self.label_log.setGeometry(QtCore.QRect(30, 110, 91, 31))
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_log.setFont(self.font)
        self.label_log.setObjectName("label_log")
        self.layout.addWidget(self.label_log)

        # Log textBrowser
        self.textBrowser_log = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_log.setGeometry(QtCore.QRect(30, 140, 741, 56))
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.layout.addWidget(self.textBrowser_log)

        # Debugger label
        self.label_debugger = QtWidgets.QLabel(self.centralwidget)
        self.label_debugger.setGeometry(QtCore.QRect(30, 200, 91, 31))
        self.label_debugger.setFont(self.font)
        self.label_debugger.setObjectName("label_debugger")
        self.layout.addWidget(self.label_debugger)

        # Debugger textBrowser
        self.textBrowser_debugger = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_debugger.setGeometry(QtCore.QRect(30, 240, 741, 281))
        self.textBrowser_debugger.setObjectName("textBrowser_debugger")
        self.layout.addWidget(self.textBrowser_debugger)

        # Set central widget
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.adaface_button.setText(_translate("MainWindow", "Start FR"))
        self.label.setText(_translate("MainWindow", "Target Person"))

        self.person_comboBox.setItemText(0, _translate("MainWindow", ""))
        self.person_comboBox.setItemText(1, _translate("MainWindow", "Person 1"))
        self.person_comboBox.setItemText(2, _translate("MainWindow", "Person 2"))
        self.person_comboBox.setItemText(3, _translate("MainWindow", "-"))
        self.person_comboBox.setItemText(4, _translate("MainWindow", "-"))

        self.person_button.setText(_translate("MainWindow", "Reset"))
        self.label_log.setText(_translate("MainWindow", "Log: "))
        self.label_debugger.setText(_translate("MainWindow", "Debug: "))


class Myagv_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Myagv_Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('moiro Test Tool')


def main(args=None):
    import sys
    app = QApplication(sys.argv)
    main_window = Myagv_Window()
    main_window.show()
    sys.exit(app.exec_())
