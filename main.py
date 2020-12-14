# -*- coding:utf-8 -*-
from PyQt5 import QtCore, QtGui, QtMultimedia
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys,socket,os,threading, time, wave, PyQt5
from utils import *
from encode import encode

class window:
    def __init__(self):
        self.main_window = loadUi("mainwindow.ui")
        self.sound = None
        self.main_window.generate_button.clicked.connect(self.handle_generate)
        self.main_window.chose_button.clicked.connect(self.handle_chose_file)
        self.main_window.play_button.clicked.connect(self.handle_play_file)
        self.main_window.stop_button.clicked.connect(self.handle_stop_file)
        self.main_window.show()

    def handle_generate(self):
        code = str2code(self.main_window.message.text())
        encode(code)

    def handle_play_file(self):
        self.sound = PyQt5.QtMultimedia.QSound(self.main_window.file_name.text())
        self.sound.play()

    def handle_stop_file(self):
        if self.sound is None:
            return
        self.sound.stop()

    def handle_chose_file(self):
        local_path, ftype = QFileDialog.getOpenFileName(self.main_window.centralwidget, "Chose a wav File", './')
        self.main_window.file_name.setText(local_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = window()
    sys.exit(app.exec_())