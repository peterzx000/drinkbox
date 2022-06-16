import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QPushButton
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtCore import pyqtSlot,QThread, pyqtSignal
import cv2
from cv2 import QT_PUSH_BUTTON

class UI:

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.widget = QWidget()

        self.start = QPushButton(self.widget)
        self.start.setText('Start')
        self.start.move(1920/10,1080/10*8)

        self.stop = QPushButton(self.widget)
        self.stop.setText('stop')
        self.stop.move(1920/10*8,1080/10*8)

        self.textLabel = QLabel(self.widget)
        self.textLabel.move(1920/10,1080/10)

        self.widget.setGeometry(0,0,1920,1080)
        self.widget.setWindowTitle("PyQt5 Example")
        self.show_image('download.png')
    
    def show_image(self,image):
        img = cv2.imread('download.png')
        h,w,c = img.shape
        qimg = QImage(img, w, h, w*3, QImage.Format_RGB888).rgbSwapped()
        self.textLabel.setPixmap(QPixmap.fromImage(qimg))

    def show(self):
        self.widget.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
   UI = UI()
   UI.show()