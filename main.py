# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updated.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
import argparse
import json
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog

import Encoder.encoder as en
import Train.train as tr
from Planner.neuralplanner import *

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self, parent):  # super().__init__(parent)
        super().__init__(parent)
        self.setupUi()
        # self.show()
        self.filename = None

    def setupUi(self):
        super().setObjectName("Dialog")
        super().resize(660, 493)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 460, 651, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnLoadConfig = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnLoadConfig.setObjectName("btnLoadConfig")
        self.btnLoadConfig.pressed.connect(self.load_config)
        self.horizontalLayout.addWidget(self.btnLoadConfig)
        self.btnDiscardClose = QtWidgets.QPushButton(
            self.horizontalLayoutWidget)
        self.btnDiscardClose.setObjectName("btnDiscardClose")
        self.btnDiscardClose.pressed.connect(self.close)
        self.horizontalLayout.addWidget(self.btnDiscardClose)
        self.btnSAve = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnSAve.setObjectName("btnSAve")
        self.btnSAve.pressed.connect(self.save_file)
        self.horizontalLayout.addWidget(self.btnSAve)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 651, 451))
        self.textEdit.setTabChangesFocus(False)
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(super())
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnLoadConfig.setText(_translate("Dialog", "Load Configration"))
        self.btnDiscardClose.setText(_translate("Dialog", "Discard and Close"))
        self.btnSAve.setText(_translate("Dialog", "Save and Close"))

    def load_config(self):
        # file_path = QFileDialog.getOpenFileUrl(None, "Open config File", '.', "(*.json)")
        self.filename, _filter = QFileDialog.getOpenFileName(
            self, "open config file", filter="*.json")
        # QMessageBox.about(None, "message", filename)
        with open(self.filename) as configfile:
            text = json.load(configfile)
            self.textEdit.setText(str(text))

    def close_file(self):
        self.close()

    def save_file(self):
        if self.filename is not None:
            with open(self.filename, 'w') as configfile:
                json.dump(eval(self.textEdit.toPlainText()), configfile)
        else:
            QMessageBox.about(
                self, "Exception", "Please load a json file to save configration settings")
        self.close()


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Environment = None
        self.window = uic.loadUi("updated.ui", self)
        self.dimension = -1
        self.dataset_path = None
        self.window.btnPlanningSpace.clicked.connect(self.btnPlanningSpace_clicked)
        self.window.btnUpdateConfigration.clicked.connect(self.btnUpdateConfigration_clicked)
        self.window.btnGenerateData.clicked.connect(self.btnGenerateData_clicked)
        self.window.btnLoadData.clicked.connect(self.btnLoadData_clicked)
        self.window.btnStartTraining.clicked.connect(self.btnStartTraining_clicked)
        self.window.btnLoadEnvironment.clicked.connect(self.btnLoadEnvironment_clicked)
        self.window.btnQuery.clicked.connect(self.btnQuery_clicked)
        self.window.btnComputePath.clicked.connect(self.btnComputePath_clicked)
        self.window.btnGenerateTaskFile.clicked.connect(self.btnGenerateTaskFile_clicked)

    def btnUpdateConfigration_clicked(self):
        print("EditConfigFile call successfully")
        ex = Ui_Dialog(self)
        ex.show()

    def btnGenerateData_clicked(self):
        os.system("""
               python3 ~/catkin_ws/src/Training_Data_Generator/data_handler.py ~/catkin_ws/src/Training_Data_Generator/config.json
               """)

    def btnLoadData_clicked(self):
        self.dataset_path = self.browse_directory()

    def btnLoadEnvironment_clicked(self):
        self.Environment = self.browse_directory()

    def btnQuery_clicked(self):
        pass
        # TODO: This should take intial and goal state and set
        #  it as a planning query. By now the planning query is set randomly.

    def btnComputePath_clicked(self):
        if self.dimension == -1:
            QMessageBox.about(None, 'Confirmation', 'Please select planning space')
        else:
            message_box = QMessageBox(QMessageBox.Question, "Confirm Download", f"Are you sure you want to Continue "
                                                                                f"with {self.dimension} Planning "
                                                                                f"space?")
            message_box.addButton(QMessageBox.Yes)
            message_box.addButton(QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)
            print(self.dimension,"line 137")
            reply = message_box.exec()

            if reply == QMessageBox.Yes and self.Environment is not None:
                #print("")
                main(self.dimension, self.NeuralPlannerPBar, self.Environment)
            else:
                QMessageBox.about(None, 'Error', 'Please select planning space and Environment path')


    def btnGenerateTaskFile_clicked(self):
        pass
        os.system("")

    def btnPlanningSpace_clicked(self):
        self.dimension = QInputDialog.getInt(
            None, 'selection Dialog', 'select Planning space:', min=2, max=3)[0]
        print(self.dimension)

    @staticmethod
    def browse_directory():
        path = QFileDialog.getExistingDirectory(None, "select folder")
        return path

    @staticmethod
    def browse_files():
        return QFileDialog.getOpenFileName(None, "select file", os.getcwd(), filter="All Files (*);;")

    def btnStartTraining_clicked(self):
        print(self.dimension)
        print("Hello World")
        en.main(self.dataset_path,
                self.dimension, self.EncodingPBar, self.EncoderDataLoaderPBar)
        tr.main(self.dataset_path,
                self.dimension, self.TrainingProgressBar, self.TrainingDataLoaderPBar)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UiMainWindow()
    ui.show()
    sys.exit(app.exec_())
