# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myagv_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set font
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.font.setWeight(75)

        # 카메라 화면을 위한 QLabel 추가
        self.camera_name = QtWidgets.QLabel(self.centralwidget)
        self.camera_name.setGeometry(QtCore.QRect(50, 30, 100, 40))
        self.camera_name.setFont(self.font)
        self.camera_name.setObjectName("camera_name")

        self.camera_label = QLabel(self.centralwidget)
        self.camera_label.setGeometry(QtCore.QRect(50, 70, 600, 400))

        # Dbg image label
        self.dbg_name = QtWidgets.QLabel(self.centralwidget)
        self.dbg_name.setGeometry(QtCore.QRect(50, 480, 150, 40))
        self.dbg_name.setFont(self.font)
        self.dbg_name.setObjectName("dbg_name")

        self.dbg_image_label = QLabel(self.centralwidget)
        self.dbg_image_label.setGeometry(QtCore.QRect(50, 520, 600, 400))

        ################
        # Adface start button
        self.adaface_button = QtWidgets.QPushButton(self.centralwidget)
        self.adaface_button.setGeometry(QtCore.QRect(740, 50, 200, 80))
        self.adaface_button.setFont(self.font)
        self.adaface_button.setStyleSheet("QPushButton:pressed{\n"
                                          "   background-color:#c7c7d0;\n"
                                          "}\n"
                                          "")
        self.adaface_button.setObjectName("adaface_button")

        # Human follower button
        self.follower_button = QtWidgets.QPushButton(self.centralwidget)
        self.follower_button.setGeometry(QtCore.QRect(740, 150, 200, 80))
        self.follower_button.setFont(self.font)
        self.follower_button.setStyleSheet("QPushButton:pressed{\n"
                                         "   background-color:#c7c7d0;\n"
                                         "}\n"
                                         "")
        self.follower_button.setObjectName("follower_button")

         ################
        # Adface reset button
        self.reset_fr = QtWidgets.QPushButton(self.centralwidget)
        self.reset_fr.setGeometry(QtCore.QRect(1350, 50, 200, 80))
        self.reset_fr.setFont(self.font)
        self.reset_fr.setStyleSheet("QPushButton:pressed{\n"
                                          "   background-color:#c7c7d0;\n"
                                          "}\n"
                                          "")
        self.reset_fr.setObjectName("reset_fr")

        # Human follower reset button
        self.reset_hf = QtWidgets.QPushButton(self.centralwidget)
        self.reset_hf.setGeometry(QtCore.QRect(1350, 150, 200, 80))
        self.reset_hf.setFont(self.font)
        self.reset_hf.setStyleSheet("QPushButton:pressed{\n"
                                         "   background-color:#c7c7d0;\n"
                                         "}\n"
                                         "")
        self.reset_hf.setObjectName("reset_hf")

        ################
        # Target person label
        self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setGeometry(QtCore.QRect(30, 60, 100, 41))
        self.label.setGeometry(QtCore.QRect(1000, 40, 100, 40))
        self.label.setFont(self.font)
        self.label.setObjectName("label")

        # Person select comboBox
        self.person_comboBox = QtWidgets.QComboBox(self.centralwidget)
        # self.person_comboBox.setGeometry(QtCore.QRect(270, 50, 100, 41))
        self.person_comboBox.setGeometry(QtCore.QRect(1000, 80, 300, 40))
        self.person_comboBox.setFont(self.font)
        self.person_comboBox.setObjectName("person_comboBox")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        self.person_comboBox.addItem("")
        ################

        # Target depth label
        self.depth_label = QtWidgets.QLabel(self.centralwidget)
        self.depth_label.setGeometry(QtCore.QRect(1000, 130, 100, 40))
        self.depth_label.setFont(self.font)
        self.depth_label.setObjectName("depth_label")
        
        self.depth_min_label = QtWidgets.QLabel(self.centralwidget)
        self.depth_min_label.setGeometry(QtCore.QRect(1000, 150, 100, 40))
        self.font.setBold(False)
        self.font.setWeight(50)
        self.depth_min_label.setFont(self.font)
        self.depth_min_label.setObjectName("depth_min_label")

        self.depth_max_label = QtWidgets.QLabel(self.centralwidget)
        self.depth_max_label.setGeometry(QtCore.QRect(1170, 150, 100, 40))
        self.depth_max_label.setFont(self.font)
        self.depth_max_label.setObjectName("depth_max_label")

        # Depth select input
        self.depth_min_input = QtWidgets.QLineEdit(self.centralwidget)
        self.depth_min_input.setGeometry(QtCore.QRect(1000, 180, 150, 40))
        self.depth_min_input.setFont(self.font)
        self.depth_min_input.setObjectName("depth_min_input")

        self.depth_max_input = QtWidgets.QLineEdit(self.centralwidget)
        self.depth_max_input.setGeometry(QtCore.QRect(1170, 180, 150, 40))
        self.depth_max_input.setFont(self.font)
        self.depth_max_input.setObjectName("depth_max_input")

        ################

        # Log label
        self.label_log = QtWidgets.QLabel(self.centralwidget)
        # self.label_log.setGeometry(QtCore.QRect(30, 110, 91, 31))
        self.label_log.setGeometry(QtCore.QRect(740, 240, 91, 31))
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_log.setFont(self.font)
        self.label_log.setObjectName("label_log")

        # Log textBrowser
        self.textBrowser_log = QtWidgets.QTextBrowser(self.centralwidget)
        # self.textBrowser_log.setGeometry(QtCore.QRect(30, 180, 741, 56))
        self.textBrowser_log.setGeometry(QtCore.QRect(740, 270, 810, 200))
        self.textBrowser_log.setObjectName("textBrowser_log")
        ################
        # Debugger label
        self.label_debugger = QtWidgets.QLabel(self.centralwidget)
        # self.label_debugger.setGeometry(QtCore.QRect(30, 200, 91, 31))
        self.label_debugger.setGeometry(QtCore.QRect(740, 480, 91, 31))
        self.label_debugger.setFont(self.font)
        self.label_debugger.setObjectName("label_debugger")

        # Debugger textBrowser
        self.textBrowser_debugger = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_debugger.setGeometry(QtCore.QRect(740, 520, 810, 400))
        self.textBrowser_debugger.setObjectName("textBrowser_debugger")
        ################
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

        self.camera_name.setText(_translate("MainWindow", "촬영 카메라"))
        self.dbg_name.setText(_translate("MainWindow", "Debugging image"))

        self.adaface_button.setText(_translate("MainWindow", "Start FR"))
        self.follower_button.setText(_translate("MainWindow", "Start HF"))

        self.label.setText(_translate("MainWindow", "Target Person"))
        self.depth_label.setText(_translate("MainWindow", "Target Depth"))
        self.depth_max_label.setText(_translate("MainWindow", "Max"))
        self.depth_min_label.setText(_translate("MainWindow", "Min"))

        self.person_comboBox.setItemText(0, _translate("MainWindow", ""))
        self.person_comboBox.setItemText(1, _translate("MainWindow", "minha"))
        self.person_comboBox.setItemText(2, _translate("MainWindow", "yeonju"))
        self.person_comboBox.setItemText(3, _translate("MainWindow", "-"))
        self.person_comboBox.setItemText(4, _translate("MainWindow", "-"))

        self.reset_fr.setText(_translate("MainWindow", "RESET FR"))
        self.reset_hf.setText(_translate("MainWindow", "RESET HF"))

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
