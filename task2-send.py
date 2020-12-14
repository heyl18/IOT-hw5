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
        user_str = self.main_window.message.text()
        sig = []
        fs = 48000
        blank_size = int(fs/4)
        sig.extend(np.zeros(2*blank_size))
        for i in range(0,len(user_str),30):
            j = 30 if i + 30 < len(user_str) else len(user_str)
            test_code = str2code(user_str[i:i+j])
            sig.extend(encode(test_code))
            sig.extend(np.zeros(2*blank_size))
        sig.extend(np.zeros(2*blank_size))
        save_wave_file(sig,'output.wav',framerate=fs)

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