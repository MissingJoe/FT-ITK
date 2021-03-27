import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QFont, QPixmap, QImage, QWheelEvent
from PyQt5.QtWidgets import QWidget, QSizePolicy

import threading
import time
import sys
import numpy as np
from tools import *


class Slice_Viewer_Widget(QWidget):
    def __init__(self, parent=None, ):
        super(Slice_Viewer_Widget, self).__init__(parent)
        self.init_UI()
        self.init_data()

        # self.data=np.load("0001.npy")
        # self.screen_width,self.screen_height,self.slices_num=self.data.shape
        # init_cover=self.data[:,:,self.slice_index]
        # showImage=array_preprocess(init_cover,-255,255)

    def init_UI(self):
        self.layout = QtWidgets.QGridLayout()
        self.label_screen = QtWidgets.QLabel(self)  # label used as a screen to display CT slices
        self.label_screen.setPixmap(
            QPixmap("GUI-resourses/start-up.PNG"))  # initialize the label_screen with start-up.PNG
        self.layout.addWidget(self.label_screen)
        self.setLayout(self.layout)
        self.setWindowTitle("Slice_Viewer_example")
        self.setWindowIcon(QIcon("GUI-resourses/FT-icon.png"))

    def init_data(self):
        self.data = None
        self.screen_width, self.screen_height, self.slices_num = None, None, None
        self.slice_index = 0

    def load_data(self, file_path):
        if ".npy" in file_path:  # numpy_file
            data = np.load(file_path)
        self.data = data
        self.screen_width, self.screen_height, self.slices_num = data.shape
        self.slice_index = 0  # initialize the slice index with 0
        self.show_a_slice()

    def show_a_slice(self, mode="others"):
        """
        display a slice onto the label screen, this function would be called when the user scrolls the mouse or loads a file
        The slice would be fetched from a self.data (3-dimention array) according to the slice_index.

        :param mode: this parameter has three possibile value:
                    "up" ---- mouse scrolling up, then slice_index+=1
                    "down" ---- mouse scrolling down, then slice_index=-1
                    "others" ---- slice_index stays the same

        :return:
        """
        if self.data is not None:
            if mode == "up":
                if self.slice_index + 1 >= self.slices_num:
                    print("currently already at the top of slices")
                else:
                    self.slice_index += 1
                    array = self.data[:, :, self.slice_index]
                    array = array_preprocess(array, -255, 255)
                    self.label_screen.setPixmap(QPixmap(array))
            elif mode == "down":
                if self.slice_index - 1 < 0:
                    print("currently already at the bottom of slices")
                else:
                    self.slice_index -= 1
                    array = self.data[:, :, self.slice_index]
                    array = array_preprocess(array, -255, 255)
                    self.label_screen.setPixmap(QPixmap(array))
            else:  # neither "up" nor "down", this situation would occur when it loads data.
                array = self.data[:, :, self.slice_index]
                array = array_preprocess(array, -255, 255)
                self.label_screen.setPixmap(QPixmap(array))
        else:
            print("No data has been loaded!")

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:      #mouse scrolling up
            print("up")
            self.show_a_slice(mode="up")
        else:                               #mouse scrolling down
            print("down")
            self.show_a_slice(mode="down")
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Slice_Viewer_Widget()
    gui.show()
    sys.exit(app.exec_())
